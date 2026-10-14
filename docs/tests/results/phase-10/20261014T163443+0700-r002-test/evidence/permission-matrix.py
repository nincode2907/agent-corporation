"""Pure permission engine checks; no DB, executor, gateway or inference."""
from datetime import UTC, datetime, timedelta
from agent_corporation_api.modules.governance.permission import evaluate_action
now=datetime.now(UTC)
base={"policy":{"automatic_actions":["read_fixture"]},"action_type":"permission_change","payload_hash":"a"*64,"environment_id":"env-a","company_id":"company-a","task_id":"task-a","task_revision":3,"run_id":"run-a","policy_id":"policy-a","policy_version":4,"within_scope":True,"now":now}
approval={"status":"approved","action_type":"permission_change","payload_hash":"a"*64,"environment_id":"env-a","company_id":"company-a","task_id":"task-a","task_revision":3,"run_id":"run-a","policy_id":"policy-a","policy_version":4,"expires_at":now+timedelta(minutes=5)}
checks={
 "exact_match_allows": evaluate_action(**{**base,"approval":approval})["allowed"] is True,
 "action_type_mismatch_denies": evaluate_action(**{**base,"action_type":"profile_change","approval":approval})["allowed"] is False,
 "revision_mismatch_denies": evaluate_action(**{**base,"task_revision":4,"approval":approval})["allowed"] is False,
 "company_mismatch_denies": evaluate_action(**{**base,"company_id":"company-b","approval":approval})["allowed"] is False,
 "environment_mismatch_denies": evaluate_action(**{**base,"environment_id":"env-b","approval":approval})["allowed"] is False,
 "payload_mismatch_denies": evaluate_action(**{**base,"payload_hash":"b"*64,"approval":approval})["allowed"] is False,
 "run_mismatch_denies": evaluate_action(**{**base,"run_id":"run-b","approval":approval})["allowed"] is False,
 "policy_mismatch_denies": evaluate_action(**{**base,"policy_version":5,"approval":approval})["allowed"] is False,
 "expired_denies": evaluate_action(**{**base,"approval":{**approval,"expires_at":now-timedelta(seconds=1)}})["allowed"] is False,
 "consumed_denies": evaluate_action(**{**base,"approval":{**approval,"consumed_at":now}})["allowed"] is False,
 "default_deny": evaluate_action(**{**base,"approval":None,"policy":None,"action_type":"tool_execution"})["allowed"] is False,
 "unknown_action_denies": evaluate_action(**{**base,"action_type":"unknown_action","approval":approval})["allowed"] is False,
}
for name,passed in checks.items(): print(f"{name}={'PASS' if passed else 'FAIL'}")
assert all(checks.values()), checks
