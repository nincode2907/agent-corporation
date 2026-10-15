"""Exercise Owner bootstrap ACLs in a temporary directory; never inspect secret bytes."""
import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[6]
spec = importlib.util.spec_from_file_location("bootstrap_owner_fixture", ROOT / "scripts" / "bootstrap_owner.py")
bootstrap_owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap_owner)

from agent_corporation_api.modules.governance.windows_acl import windows_acl_matches

with tempfile.TemporaryDirectory(prefix="ac-owner-acl-r008-") as temp:
    secret_path = bootstrap_owner.bootstrap(Path(temp))
    assert secret_path.is_file()
    assert windows_acl_matches(secret_path.parent, directory=True)
    assert windows_acl_matches(secret_path, directory=False)
    print("PASS temporary Owner bootstrap creates private protected directory/file ACL; secret content not read")
