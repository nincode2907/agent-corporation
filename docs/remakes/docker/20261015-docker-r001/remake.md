# Docker runtime — remake r001

- Trạng thái xử lý: changed
- Report nguồn: [Independent r001](../../../tests/results/docker/20261015-docker-r001/report.md).
- DKR-01: `scripts/cg01_mode.py` truyền `codex_server_transport` vào strict gate; runtime image chứa script. Synthetic Docker proof regression xác nhận release-check nhận đúng endpoint/transport, không tái sử dụng proof native.
- DKR-02: bootstrap Compose chạy theo `BOOTSTRAP_UID/GID` (mặc định 1000); launcher POSIX export UID/GID của người chạy. File host tạo mới giữ quyền sở hữu của người dùng Linux. Runtime API vẫn UID1000 với bản copy Owner secret mode0600 trong volume riêng.
- Root validation: native và Linux container cùng 99 pass/1 Windows-only skip; Docker isolated stack fresh migration/auth/CSRF/SSE/restart/session/DB-down pass, zero model calls, cleanup project tạm.
- Cần independent r002 xác minh; chưa nghiệm thu phase hoặc cấp inference grant. Windows Desktop chưa được chạy trên phần cứng Windows.
