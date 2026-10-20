"""Disposable browser rehearsal API entrypoint; never use in normal Compose."""
from agent_corporation_api.modules.governance import auth
from agent_corporation_api.modules.governance import profile
from agent_corporation_api.modules.execution import router

auth.ALLOWED_ORIGINS = auth.ALLOWED_ORIGINS | {"http://127.0.0.1:15502"}
profile.profile_model_capabilities = lambda _settings: {"synthetic.fake-transport": ["low"]}
router.gate = lambda _scope: {"allowed": True, "mode": "demo-test", "verified": False,
                              "reason": "isolated_synthetic_transport_harness"}

import uvicorn

uvicorn.run("agent_corporation_api.main:app", host="0.0.0.0", port=15501, proxy_headers=False)
