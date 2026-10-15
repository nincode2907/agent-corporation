# Commands — r009

The worker was intentionally scoped to the local demo environment/company returned by the read-only demo dashboard.

```text
rtk proxy python -X utf8 -c "import json,urllib.request; d=json.load(urllib.request.urlopen('http://127.0.0.1:15501/api/v1/demo/dashboard',timeout=5)); print(json.dumps({'available':d.get('available'),'environment_id':(d.get('environment') or {}).get('id'),'company_id':(d.get('company') or {}).get('id'),'inference_requests':d.get('inference_requests')}))"
```

The first documented module command exited before import completed (`ModuleNotFoundError: No module named 'agent_corporation_api'`); it did not run worker logic or dispatch. The corrected scoped command below exited 0, processed the already queued run once, and produced the UI evidence in `runtime-checks.md`.

```text
rtk proxy uv run --project apps/api python -c "import sys;sys.path.insert(0,'apps/api/src');from agent_corporation_api.modules.execution.worker import main;main()" --environment b93f752e-7b69-5e8b-8f74-1498a15a5609 --company b4375333-b12b-5fca-b984-87864032d3a8 --once
```

Exit code: `0`. No retry or second run was issued.
