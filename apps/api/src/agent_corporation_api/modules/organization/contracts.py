"""Organization and immutable employee-profile contracts for Phase 13.

These models do not persist profiles or open Employee Chat. Persistence is
deliberately separate while Phase 12 and the CG01 target decision are blocked.
"""
from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class OrganizationInvalid(ValueError):
    pass


class DepartmentNode(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    parent_department_id: UUID | None = None
    name: str = Field(min_length=1, max_length=120)


class EmployeeNode(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    department_id: UUID | None = None
    reports_to_employee_id: UUID | None = None
    lifecycle: Literal["active", "probation", "draining", "offboarded"]
    current_profile_version: int = Field(ge=1)


class OrganizationSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    environment_id: UUID
    company_id: UUID
    departments: list[DepartmentNode] = Field(max_length=500)
    employees: list[EmployeeNode] = Field(max_length=2000)

    @model_validator(mode="after")
    def validate_graph(self) -> "OrganizationSnapshot":
        dept_ids = [department.id for department in self.departments]
        employee_ids = [employee.id for employee in self.employees]
        if len(dept_ids) != len(set(dept_ids)) or len(employee_ids) != len(set(employee_ids)):
            raise ValueError("organization IDs must be unique within scope")

        departments = {department.id: department for department in self.departments}
        employees = {employee.id: employee for employee in self.employees}
        for department in self.departments:
            if (department.environment_id, department.company_id) != (self.environment_id, self.company_id):
                raise ValueError("cross_scope_department")
            if department.parent_department_id is not None:
                if department.parent_department_id not in departments:
                    raise ValueError("unknown_parent_department")
                if department.parent_department_id == department.id:
                    raise ValueError("department_cycle")
        for employee in self.employees:
            if (employee.environment_id, employee.company_id) != (self.environment_id, self.company_id):
                raise ValueError("cross_scope_employee")
            if employee.department_id is not None and employee.department_id not in departments:
                raise ValueError("unknown_department")
            if employee.reports_to_employee_id is not None:
                if employee.reports_to_employee_id not in employees:
                    raise ValueError("unknown_reporting_employee")
                if employee.reports_to_employee_id == employee.id:
                    raise ValueError("reporting_cycle")

        self._assert_acyclic(
            {department.id: department.parent_department_id for department in self.departments},
            "department_cycle",
        )
        self._assert_acyclic(
            {employee.id: employee.reports_to_employee_id for employee in self.employees},
            "reporting_cycle",
        )
        return self

    @staticmethod
    def _assert_acyclic(parents: dict[UUID, UUID | None], error: str) -> None:
        done: set[UUID] = set()
        for node_id in parents:
            path: set[UUID] = set()
            current: UUID | None = node_id
            while current is not None and current not in done:
                if current in path:
                    raise ValueError(error)
                path.add(current)
                current = parents.get(current)
            done.update(path)


class EmployeeProfileVersion(BaseModel):
    """One immutable profile version; caller appends a new version on change."""
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    employee_id: UUID
    version: int = Field(ge=1)
    contract_type: Literal["permanent", "on_demand", "contractor"]
    role: str = Field(min_length=1, max_length=120)
    persona: str = Field(min_length=1, max_length=4000)
    model: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9._:-]+$")
    reasoning_effort: Literal["minimal", "low", "medium", "high", "xhigh", "max", "ultra", "persistent"]
    tool_capabilities: list[str] = Field(default_factory=list, max_length=32)
    skill_refs: list[str] = Field(default_factory=list, max_length=50)
    context_refs: list[str] = Field(default_factory=list, max_length=50)
    policy_id: UUID | None = None
    policy_version: int | None = Field(default=None, ge=1)

    @field_validator("role", "persona")
    @classmethod
    def nonblank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("profile fields must not be blank")
        return value

    @field_validator("tool_capabilities")
    @classmethod
    def capabilities_are_unique(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("tool capabilities must be unique")
        if any(not value or len(value) > 100 or not value.replace(":", "").replace("_", "").replace("-", "").isalnum() for value in values):
            raise ValueError("tool capability is invalid")
        return values

    @field_validator("skill_refs", "context_refs")
    @classmethod
    def references_are_scoped(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value or len(value) > 160 or value.startswith(("/", "\\")) or ".." in value or "\\" in value:
                raise ValueError("profile references must be scoped opaque refs")
        if len(values) != len(set(values)):
            raise ValueError("profile references must be unique")
        return values

    @model_validator(mode="after")
    def policy_pin_is_complete(self) -> "EmployeeProfileVersion":
        if (self.policy_id is None) != (self.policy_version is None):
            raise ValueError("policy_id and policy_version must be set together")
        return self


def next_profile_version(*, current_version: int, expected_version: int) -> int:
    """Return append-only version number; stale edits conflict without mutation."""
    if type(current_version) is not int or current_version < 0:
        raise OrganizationInvalid("invalid_current_version")
    if type(expected_version) is not int or expected_version < 0:
        raise OrganizationInvalid("invalid_expected_version")
    if expected_version != current_version:
        raise OrganizationInvalid("stale_profile_version")
    return current_version + 1
