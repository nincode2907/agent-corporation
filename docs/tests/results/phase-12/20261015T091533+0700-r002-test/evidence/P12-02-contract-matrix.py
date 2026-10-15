"""Direct synthetic assertions for the remediated Phase 12 contracts."""
from uuid import UUID

from pydantic import ValidationError

from agent_corporation_api.modules.orchestration.contracts import (
    DelegationLimits,
    Handoff,
    OrchestrationInvalid,
)


def handoff(refs):
    return Handoff(
        parent_task_id=UUID("00000000-0000-0000-0000-000000000003"),
        subtask_id=UUID("00000000-0000-0000-0000-000000000010"),
        correlation_id=UUID("00000000-0000-0000-0000-000000000004"),
        from_employee_version_id=UUID("00000000-0000-0000-0000-000000000020"),
        to_employee_version_id=UUID("00000000-0000-0000-0000-000000000021"),
        decision_summary="Synthetic handoff summary",
        evidence_refs=refs,
    )


assert handoff(["artifact:abc123", "run:run-42"]).evidence_refs
for bad_refs in ([], [""], ["artifact:"], ["../../secret"], ["artifact:foo/bar"], ["artifact:foo..bar"]):
    try:
        handoff(bad_refs)
    except ValidationError:
        continue
    raise AssertionError("invalid evidence reference list accepted")

for field in ("max_nodes", "max_fanout", "max_depth", "max_iterations"):
    for bad_value in (True, 2.0):
        limits = {name: 2 for name in ("max_nodes", "max_fanout", "max_depth", "max_iterations")}
        limits[field] = bad_value
        try:
            DelegationLimits(**limits).validate()
        except OrchestrationInvalid as exc:
            assert str(exc) == "limits_must_be_integers"
        else:
            raise AssertionError("non-integer delegation limit accepted")

print({
    "valid_refs_accepted": True,
    "empty_and_bad_refs_rejected": True,
    "strict_integer_bool_and_float_rejected_for_all_limits": True,
})
