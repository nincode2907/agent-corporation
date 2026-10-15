# Runtime/UI checks — r010

- Source: parent-provided browser observation; no cookie/session details were accessed or recorded by this test agent.
- Route: `http://127.0.0.1:15500/#playground` in an existing authenticated browser session.
- API/web: parent restarted the API using the updated source; parent-observed readiness on `127.0.0.1:15501` returned 200 and web on `127.0.0.1:15500` returned 200.
- Observed: Playground page rendered; existing profile `gpt-6-luna · medium`, three demo employees, and form limits of 20 requests/30 minutes loaded; demo policy acceptance remained unchecked; Create Grant button was disabled; no conversation existed.
- Actions: no login automation; no grant create; no message send; no Stop, revoke, expiry, or unknown-resolution UI action.
- Inference: none in r010. The observed disabled grant action supports “page open does not automatically create a grant”; it does not verify the authorized send workflow.
- Result: DPG10 remains blocked pending explicit test grant and browser workflow evidence.
