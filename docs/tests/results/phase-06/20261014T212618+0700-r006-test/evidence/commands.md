# Retest r006 — commands và evidence

AI tester `/root/cg01_demo_review`, độc lập `/root` remake. Bắt đầu2026-10-14T21:26:18+07:00. Không đọc .env/secrets, không grant/inference/DB/sharedgateway/runtime restart.

1. `rtk proxy uv run --project apps/api --no-sync pytest apps/api/tests/test_cg01_demo_mode.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_codex_gateway.py -q`
   - Exit0: **49 passed, 8 skipped**, 1 Starlette/httpx deprecation warning,1.75s.
   - Có mới `test_release_cli_vietnamese_diagnostic_with_windows_console_encoding`: subprocess stdoutcp1252/PYTHONUTF8=0, fake settings/releasecheck; UTF8 message `CG01 release: BLOCKED · Ngoại lệ demo còn bật`, exit1, stderrempty. Không đọc realenv. P06-16 **FIX VERIFIED**.
   - Existing strict/default/demoScope/URL/Owner/grant/bodyoverride/workerrelock/toggle/limits/stop/unknown/usage regression thực sự rerun.8POSIXskip vẫn không được xem PASS proof.
2. `rtk proxy uv run --project apps/api --no-sync python -X utf8 docs/tests/results/phase-06/20261014T212618+0700-r006-test/evidence/P06-12-fixture.py`
   - Exit0: CSRF/Origin/Host/crosssite6negative; GrantInput6negative+2positive PASS; cg01_at_creation SQL JSON/checkpoint retains unverified demo PASS; worker exactly1fakeexecutor PASS. No DB/model/network/secrets.
3. Source hash comparison với r005 manifest: chỉ script `cg01_mode.py`, test `test_cg01_demo_mode.py`, generated `master-plan.html` khác. Đã đọc trực tiếp source script/test, remake, rule retest và checklist06. Product gate/auth/service/worker/UI source unchanged; xét lại paths và rerun ảnh hưởng. Không rerun web build vì fix chỉ CLI stdout/stderr; build r005 là ngữ cảnh, không evidence fresh UI.
4. `rtk proxy python -X utf8 scripts/render_plan.py`
   - Kỳ vọng report canonical24cases/r006 và ledger đồng bộ; observed final exit0 ghi khi tạo batch.

Activation đã thực hiện bởi parent tại [remake evidence](../../../../../remakes/phase-06/20261014T212353+0700-r005-remake/evidence/runtime-activation.md). Đây parent observation, không independent live status. APIproject28836 live200, readiness503, gatewayoffline theo parent; không coi có authenticated demo UI hay model call.

Full-phase blocker giữ: CG01actual isolation/privacy/cancellation, grant/live model/artifact/usage, disposable DB race/RLS/persistence, UIOwnerWindows. Không chạy validator/runtime lại; blockers là thiếu evidence hiện tại. Phiên này chỉ fixverification + focusedregression, không releaseV1.
