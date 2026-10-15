# Browser review evidence — r004

- Separate agent-owned Chrome tab opened to local `#replay`; Owner session was already authenticated in the browser profile. No secret or cookie was inspected and no login was performed.
- Environment label: DEMO / Demo Corporation / “Fixture v1 · số liệu demo fixture”.
- Replay initially listed run `100bc3c8` as completed among saved runs. Selecting that run filtered the timeline to 10 saved events (stream sequences 23–32).
- Seek: selecting the final event `LLM_CALL_COMPLETED` advanced cursor to `10 / 10`.
- Reload: “Tải lại từ đầu” retained selected run `100bc3c8` and cursor `10 / 10`; the same 10 events remained visible.
- Replay wording: “Replay chỉ đọc dữ liệu đã commit”; up to 200 events shown in the current window; “khoảng trống cần tải lại, không được nội suy.” No call replay action exists in the reviewed UI flow; no model/tool request was triggered by this reviewer.
- Inspector route showed the exact full run ID `100bc3c8-3944-4bed-94aa-770364161b3c`, completed status, model `gpt-6-luna`, effort `medium`, task ID, and 10 related events. Inspector summary explicitly said no explicit summary in the current projection; tools/file-diff/messages and profile snapshot were explicitly unavailable.
- Usage displayed total 10,435 tokens (input 10,354; output 81) and cost basis `unknown`.
- No active run was shown, and no Live Office active-agent claim is made. The historical run is from Phase 06; no Phase 08 grant is implied.
- Not exercised: dashboard/task/org alternate Inspector entry points; cross-company/environment or actor ACL negative paths; network drop/reconnect; event/API network spy; persisted DB before/after comparison; mobile/keyboard layout. Therefore corresponding criteria remain blocked.

The parent task explicitly disallowed inference, grant creation, mutating app state, replaying calls, gateway access, and runtime database writes. UI interactions were limited to selecting the saved-run filter, navigating between Inspector and Replay, seeking a stored event, and reloading stored events.
