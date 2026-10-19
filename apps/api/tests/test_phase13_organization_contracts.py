from uuid import UUID

import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.organization.contracts import (
    DepartmentNode,
    EmployeeNode,
    EmployeeProfileVersion,
    OrganizationInvalid,
    OrganizationSnapshot,
    next_profile_version,
)


ENV = UUID("00000000-0000-0000-0000-000000000001")
COMPANY = UUID("00000000-0000-0000-0000-000000000002")
ROOT_DEPT = UUID("00000000-0000-0000-0000-000000000010")
CHILD_DEPT = UUID("00000000-0000-0000-0000-000000000011")
EMPLOYEE = UUID("00000000-0000-0000-0000-000000000020")
MANAGER = UUID("00000000-0000-0000-0000-000000000021")


def dept(dept_id: UUID, parent_id: UUID | None = None, *, company_id: UUID = COMPANY):
    return DepartmentNode(
        id=dept_id,
        environment_id=ENV,
        company_id=company_id,
        parent_department_id=parent_id,
        name=f"Department {str(dept_id)[-2:]}",
    )


def employee(
    employee_id: UUID,
    *,
    department_id: UUID | None = None,
    manager_id: UUID | None = None,
    company_id: UUID = COMPANY,
):
    return EmployeeNode(
        id=employee_id,
        environment_id=ENV,
        company_id=company_id,
        department_id=department_id,
        reports_to_employee_id=manager_id,
        lifecycle="active",
        current_profile_version=1,
    )


def profile(**overrides):
    data = {
        "employee_id": EMPLOYEE,
        "version": 1,
        "contract_type": "permanent",
        "role": "Researcher",
        "persona": "Careful and concise.",
        "model": "model-profile-ref",
        "reasoning_effort": "medium",
        "tool_capabilities": ["workspace:read"],
        "skill_refs": ["skill:research"],
        "context_refs": ["context:company-policy"],
        "policy_id": UUID("00000000-0000-0000-0000-000000000030"),
        "policy_version": 2,
    }
    data.update(overrides)
    return EmployeeProfileVersion(**data)


def test_same_scope_department_and_reporting_graph_is_valid():
    snapshot = OrganizationSnapshot(
        environment_id=ENV,
        company_id=COMPANY,
        departments=[dept(ROOT_DEPT), dept(CHILD_DEPT, ROOT_DEPT)],
        employees=[
            employee(MANAGER, department_id=ROOT_DEPT),
            employee(EMPLOYEE, department_id=CHILD_DEPT, manager_id=MANAGER),
        ],
    )
    assert len(snapshot.departments) == 2
    assert len(snapshot.employees) == 2


@pytest.mark.parametrize(
    "departments,employees,match",
    [
        ([dept(ROOT_DEPT, CHILD_DEPT), dept(CHILD_DEPT, ROOT_DEPT)], [], "department_cycle"),
        ([dept(ROOT_DEPT)], [employee(EMPLOYEE, manager_id=MANAGER), employee(MANAGER, manager_id=EMPLOYEE)], "reporting_cycle"),
        ([dept(ROOT_DEPT)], [employee(EMPLOYEE, department_id=CHILD_DEPT)], "unknown_department"),
        ([dept(ROOT_DEPT)], [employee(EMPLOYEE, manager_id=MANAGER)], "unknown_reporting_employee"),
    ],
)
def test_cycles_and_dangling_organization_references_are_rejected(departments, employees, match):
    with pytest.raises(ValidationError, match=match):
        OrganizationSnapshot(
            environment_id=ENV, company_id=COMPANY, departments=departments, employees=employees
        )


def test_cross_environment_or_company_members_are_rejected():
    with pytest.raises(ValidationError, match="cross_scope_department"):
        OrganizationSnapshot(
            environment_id=ENV,
            company_id=COMPANY,
            departments=[dept(ROOT_DEPT, company_id=UUID("00000000-0000-0000-0000-000000000099"))],
            employees=[],
        )
    with pytest.raises(ValidationError, match="cross_scope_employee"):
        OrganizationSnapshot(
            environment_id=ENV,
            company_id=COMPANY,
            departments=[],
            employees=[employee(EMPLOYEE, company_id=UUID("00000000-0000-0000-0000-000000000099"))],
        )


def test_profile_versions_validate_pins_and_scoped_refs():
    version = profile()
    assert version.version == 1
    assert profile(contract_type="on_demand").contract_type == "on_demand"
    assert profile(contract_type="contractor").contract_type == "contractor"
    with pytest.raises(ValidationError, match="frozen"):
        version.role = "Changed by worker"
    with pytest.raises(ValidationError):
        profile(tool_capabilities=["workspace:read", "workspace:read"])
    with pytest.raises(ValidationError):
        profile(skill_refs=["../../private"])
    with pytest.raises(ValidationError):
        profile(role=" ")
    with pytest.raises(ValidationError, match="set together"):
        profile(policy_id=None)
    with pytest.raises(ValidationError):
        EmployeeProfileVersion.model_validate({**profile().model_dump(), "is_owner_approved": True})


def test_profile_revision_is_append_only_and_stale_writes_conflict():
    assert next_profile_version(current_version=1, expected_version=1) == 2
    with pytest.raises(OrganizationInvalid, match="stale_profile_version"):
        next_profile_version(current_version=2, expected_version=1)
    with pytest.raises(OrganizationInvalid, match="invalid_current_version"):
        next_profile_version(current_version=True, expected_version=1)
