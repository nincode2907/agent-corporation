"""Windows ACL checks for local Owner credentials.

The Windows equivalent of a 0600 secret is a protected DACL containing one
allow ACE for the current process user. The .local directory receives one
full-control ACE that is inheritable by its children.
"""
from __future__ import annotations

import ctypes
import os
from ctypes import wintypes
from pathlib import Path


SE_FILE_OBJECT = 1
DACL_SECURITY_INFORMATION = 0x00000004
PROTECTED_DACL_SECURITY_INFORMATION = 0x80000000
SE_DACL_PROTECTED = 0x1000
TOKEN_QUERY = 0x0008
TOKEN_USER_CLASS = 1
ACCESS_ALLOWED_ACE_TYPE = 0
OBJECT_INHERIT_ACE = 0x01
CONTAINER_INHERIT_ACE = 0x02
FILE_GENERIC_READ = 0x00120089
FILE_ALL_ACCESS = 0x001F01FF


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", wintypes.DWORD)]


class _TokenUser(ctypes.Structure):
    _fields_ = [("User", _SidAndAttributes)]


class _Acl(ctypes.Structure):
    _fields_ = [
        ("AclRevision", wintypes.BYTE),
        ("Sbz1", wintypes.BYTE),
        ("AclSize", wintypes.WORD),
        ("AceCount", wintypes.WORD),
        ("Sbz2", wintypes.WORD),
    ]


class _AceHeader(ctypes.Structure):
    _fields_ = [
        ("AceType", wintypes.BYTE),
        ("AceFlags", wintypes.BYTE),
        ("AceSize", wintypes.WORD),
    ]


def _apis():
    if os.name != "nt":
        raise OSError("Windows ACLs are only available on Windows")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p
    advapi32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    advapi32.GetTokenInformation.restype = wintypes.BOOL
    advapi32.ConvertSidToStringSidW.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.LPWSTR)]
    advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD)]
    advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL
    advapi32.GetSecurityDescriptorDacl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.BOOL), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.BOOL)]
    advapi32.GetSecurityDescriptorDacl.restype = wintypes.BOOL
    advapi32.SetNamedSecurityInfoW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    advapi32.SetNamedSecurityInfoW.restype = wintypes.DWORD
    advapi32.GetNamedSecurityInfoW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]
    advapi32.GetNamedSecurityInfoW.restype = wintypes.DWORD
    advapi32.GetSecurityDescriptorControl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.WORD), ctypes.POINTER(wintypes.DWORD)]
    advapi32.GetSecurityDescriptorControl.restype = wintypes.BOOL
    advapi32.GetAce.argtypes = [ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p)]
    advapi32.GetAce.restype = wintypes.BOOL
    advapi32.EqualSid.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    advapi32.EqualSid.restype = wintypes.BOOL
    return kernel32, advapi32


def _current_user_sid() -> str:
    kernel32, advapi32 = _apis()
    token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(token)):
        raise ctypes.WinError(ctypes.get_last_error())
    token_buffer = ctypes.create_string_buffer(1024)
    try:
        returned = wintypes.DWORD()
        if not advapi32.GetTokenInformation(
            token, TOKEN_USER_CLASS, token_buffer, len(token_buffer), ctypes.byref(returned)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        sid_ptr = ctypes.cast(token_buffer, ctypes.POINTER(_TokenUser)).contents.User.Sid
        sid_text = wintypes.LPWSTR()
        if not advapi32.ConvertSidToStringSidW(sid_ptr, ctypes.byref(sid_text)):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            return sid_text.value
        finally:
            kernel32.LocalFree(ctypes.cast(sid_text, ctypes.c_void_p))
    finally:
        kernel32.CloseHandle(token)


def _security_descriptor(path: Path):
    _kernel32, advapi32 = _apis()
    owner = ctypes.c_void_p()
    group = ctypes.c_void_p()
    acl = ctypes.c_void_p()
    sacl = ctypes.c_void_p()
    descriptor = ctypes.c_void_p()
    status = advapi32.GetNamedSecurityInfoW(
        str(path),
        SE_FILE_OBJECT,
        DACL_SECURITY_INFORMATION,
        ctypes.byref(owner),
        ctypes.byref(group),
        ctypes.byref(acl),
        ctypes.byref(sacl),
        ctypes.byref(descriptor),
    )
    if status:
        raise ctypes.WinError(status)
    return descriptor, acl


def secure_windows_acl(path: Path, *, directory: bool) -> None:
    """Set a protected, current-user-only DACL on a file or directory."""
    kernel32, advapi32 = _apis()
    sid = _current_user_sid()
    acl = "D:P(A;OICI;0x001f01ff;;;" + sid + ")" if directory else "D:P(A;;0x00120089;;;" + sid + ")"
    descriptor = ctypes.c_void_p()
    size = wintypes.DWORD()
    if not advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        acl, 1, ctypes.byref(descriptor), ctypes.byref(size)
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    dacl_ptr = ctypes.c_void_p()
    present = wintypes.BOOL()
    defaulted = wintypes.BOOL()
    try:
        if not advapi32.GetSecurityDescriptorDacl(
            descriptor, ctypes.byref(present), ctypes.byref(dacl_ptr), ctypes.byref(defaulted)
        ) or not present.value or not dacl_ptr.value:
            raise OSError("Windows did not build the requested Owner ACL")
        status = advapi32.SetNamedSecurityInfoW(
            str(path),
            SE_FILE_OBJECT,
            DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION,
            None,
            None,
            dacl_ptr,
            None,
        )
        if status:
            raise ctypes.WinError(status)
    finally:
        kernel32.LocalFree(descriptor)
    if not windows_acl_matches(path, directory=directory):
        raise OSError("Owner ACL verification failed")


def windows_acl_matches(path: Path, *, directory: bool) -> bool:
    """Require a protected DACL with one exact ACE for the current user."""
    if os.name != "nt" or path.is_symlink():
        return False
    kernel32, advapi32 = _apis()
    try:
        descriptor, acl = _security_descriptor(path)
    except OSError:
        return False
    if not descriptor.value or not acl.value:
        return False
    try:
        control = wintypes.WORD()
        revision = wintypes.DWORD()
        if not advapi32.GetSecurityDescriptorControl(descriptor, ctypes.byref(control), ctypes.byref(revision)):
            return False
        if not control.value & SE_DACL_PROTECTED:
            return False
        header = ctypes.cast(acl, ctypes.POINTER(_Acl)).contents
        if header.AceCount != 1:
            return False
        ace = ctypes.c_void_p()
        if not advapi32.GetAce(acl, 0, ctypes.byref(ace)) or not ace.value:
            return False
        ace_header = ctypes.cast(ace, ctypes.POINTER(_AceHeader)).contents
        expected_flags = OBJECT_INHERIT_ACE | CONTAINER_INHERIT_ACE if directory else 0
        if ace_header.AceType != ACCESS_ALLOWED_ACE_TYPE or ace_header.AceFlags != expected_flags:
            return False
        mask = ctypes.c_uint32.from_address(ace.value + ctypes.sizeof(_AceHeader)).value
        expected_mask = FILE_ALL_ACCESS if directory else FILE_GENERIC_READ
        if mask != expected_mask:
            return False
        sid_ptr = ctypes.c_void_p(ace.value + ctypes.sizeof(_AceHeader) + ctypes.sizeof(wintypes.DWORD))
        token = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(token)):
            return False
        token_buffer = ctypes.create_string_buffer(1024)
        returned = wintypes.DWORD()
        try:
            if not advapi32.GetTokenInformation(token, TOKEN_USER_CLASS, token_buffer, len(token_buffer), ctypes.byref(returned)):
                return False
            user_sid = ctypes.cast(token_buffer, ctypes.POINTER(_TokenUser)).contents.User.Sid
            return bool(advapi32.EqualSid(user_sid, sid_ptr))
        finally:
            kernel32.CloseHandle(token)
    finally:
        kernel32.LocalFree(descriptor)
