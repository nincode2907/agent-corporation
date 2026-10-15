# Runtime checks — r009

- Browser: Owner authenticated at `http://127.0.0.1:15500/#settings`; scope `b4375333…`.
- Model profile: `gpt-6-luna`, `medium`, version 1.
- Gateway: prior UI probe health/catalog succeeded; probe itself made GET only.
- Grant UI: created Phase 06 grant `phase06-ui-b4375333`, 1 request, 120 seconds, no requeues, concurrency 1, tools disabled, 15-minute expiry. UI explicitly reported no model call at grant time.
- Run: `100bc3c8-3944-4bed-94aa-770364161b3c`; UI showed completed/final_response at 23:30:05. Run was dispatched by scoped worker `--once`.
- Output visible in UI: “Vì lần gọi trước có thể đã thực hiện hành động dù phản hồi bị mất; retry mù quáng có thể gây tác dụng phụ hoặc xử lý trùng lặp. Chỉ nên retry khi xác định thao tác an toàn lặp lại hoặc có cơ chế idempotency để ngăn lặp.”
- Usage visible in UI: prompt 10,354; completion 81; total 10,435; cached tokens 0; reasoning tokens 0. Cost remains unknown.
- UI event feed: `OWNER_MODEL_PROFILE_UPDATED` → `EXECUTION_GRANT_CREATED` → `RUN_CREATED` → `TASK_STARTED`/`LLM_CALL_STARTED` → `TOKEN_USAGE_RECORDED` → `LLM_CALL_COMPLETED`; run ID linked in displayed event entries.
- Reloaded grant selector reported “Chưa có grant hợp lệ”, consistent with one used request and no remaining request capacity.
- CG01 UI reported temporary demo override and explicitly `chưa xác minh CG01`; no isolation proof was produced.
- Runtime dashboard fixture count still displayed `inference 0`; this is not the runtime ledger and does not contradict the completed Phase 06 run/events. Cost/ledger rollup was not checked.
- No secret, cookie, token, or prompt containing private data was recorded in this file.
