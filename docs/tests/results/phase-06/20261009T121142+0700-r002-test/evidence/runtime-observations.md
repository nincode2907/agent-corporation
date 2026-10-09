# Evidence kiểm định độc lập r002

Môi trường PG disposable `agent-corporation-qa067-disposable`, label phase06-07, image postgres18.6 pinned đúng compose, chỉ loopback Docker random50822, DBqa067; fake canary credentials, fake Ownersecret0600 tại /private/tmp. Settings.env_file=None trước pytest/Alembic; không đọc .env hoặc gateway. Không gọi inference. Migration fresh→head20261009_0005 PASS. API57tests:56pass1fail. Independent API/PG3cases:1pass2fail. Auth durable workflow PASS: scope substitution403, unauth401, CSRF403, profileCAS409, expiry/logout401, hashes khác plaintext, event/profile committed. Initial secret /tmp bị deny503 vì symlink; đổi sang /private/tmp fixture, không thay productguard.

Confirmed failures:
- C07/P06-08: read runtime runs_list locks/inserts counter and FK fails for missingcompany; reads should be readonly. Initial fullsuite exit1.
- P06-05/P06-07: completed(fake) with usage=None releases guard; samegrantmaxrequests2 allows secondreservation. Independentcase exit1.
- P06-02: proof JSON[] .get raisesAttributeError instead of denied metadata. Independentcase exit1. NonregularFIFOopen may block (source risk, not executed).
- P06-08: runtime updates only run_execution_state, task_execution_state staysqueued after waiting/completed/cancelled; task lifecycle needs transition/event distinct from acceptance (code verified).

Live CG01/inference remains blocked: no Ownergrant for actualbatch, no isolation/privacy/cancellation proof; no fake success substitutes livecases.
