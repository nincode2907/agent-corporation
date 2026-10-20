# Integration Fix 05.1 — Shared deployment preflight

**Kiểm tra chỉ đọc:** 20/10/2026 (Asia/Ho_Chi_Minh). Không build/restart container, không migrate shared DB, không reset/seed, không đọc/in ra secret.

## Trạng thái được quan sát

| Hạng mục | Kết quả |
|---|---|
| Shared Compose services đang chạy | PostgreSQL, API, Nginx web; cả ba healthy. Bootstrap/migrate là one-shot đã kết thúc. Không có container Runtime worker đang chạy. |
| Compose source hiện tại | Có service `worker`, phụ thuộc bootstrap/migration, `restart: unless-stopped`; advisory lock PostgreSQL của worker giữ trên cùng physical connection. Compose có đúng một service worker cho demo scope. |
| Volume | PostgreSQL đang dùng volume `agent-corporation_agent_corporation_postgres`; API dùng volume `runtime_secrets` và `artifacts`; PG dùng `database_secrets`. Không có lệnh xóa volume được chạy. |
| Migration | Shared DB `alembic_version=20261014_0009`; migration mới `20261020_0010` chỉ tạo bảng decision append-only, RLS, FK, unique idempotency và quyền SELECT/INSERT. |
| Demo data | Fixed-scope `Demo Corporation` vẫn khớp ID/environment đã provision; có 3 employee. Chỉ truy vấn existence/count, không đọc profile hay seed/reset. |
| Runtime ledger | 0 `runtime_runs`, 0 `model_calls`, 0 grant còn hạn mức; dispatch guard trống. Không có Runtime call đang chờ được worker mới dispatch trong ledger hiện tại. |
| Queue khác | Có các trạng thái Work Order trong `run_execution_state`; Runtime worker không phải Work Order executor và không bridge queue này. |
| Health | API readiness HTTP 200; web HTTP 200; PostgreSQL healthy. Gateway `GET /health`: HTTP 200, `active_requests=0`, `queued_requests=0`. |
| CG01 | Đọc policy từ container cho demo scope: `strict`, `allowed=false`, `verified=false`, `missing_or_invalid_proof`. Không bật ngoại lệ. |

Lệnh truy vấn migration/state chỉ in revision và counts, không in credential hay nội dung demo. Manifest evidence ở `evidence/deployment-preflight.json`.

## Rủi ro tương thích

- Shared container images chưa chứa source Fix 05/05.1; shared DB còn revision 0009. UI/API hiện chạy là phiên bản trước các thay đổi đang có trong checkout.
- `worker` có trong Compose source nhưng chưa active trong shared deployment. Sau khi chạy Compose, worker sẽ tự khởi động. Khởi động này không gọi model nếu strict CG01 hoặc grant chặn; tuy vậy worker có thể kiểm tra/recover lease theo thiết kế. Preflight hiện không thấy Runtime run/call hoặc grant hợp lệ.
- Migration mới thêm schema, không sửa/xóa dữ liệu hiện có. Bootstrap giữ config/Owner credential trong volume nếu config cũ hợp lệ. Không dùng `docker compose down --volumes`; không reseed.
- `docker compose up --build` có thể thay API/web và chạy migration; không chạy trong đợt này vì brief yêu cầu Owner duyệt trước. Không restart gateway hay shared infrastructure khác.

## Quy trình dự kiến sau khi Owner duyệt deploy

Chạy tại root repo và giữ nguyên project/volumes hiện có:

```bash
rtk proxy docker compose up --build
```

Sau khi các service healthy, kiểm tra riêng:

```bash
rtk proxy docker compose ps
rtk proxy docker compose exec -T postgres sh -ec 'set -a; . /database-secrets/postgres.env; set +a; psql -X -A -t -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version_num FROM alembic_version"'
rtk proxy docker compose exec -T postgres sh -ec 'set -a; . /database-secrets/postgres.env; set +a; psql -X -A -t -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT (SELECT count(*) FROM companies WHERE id = '\''b4375333-b12b-5fca-b984-87864032d3a8'\''::uuid AND environment_id = '\''b93f752e-7b69-5e8b-8f74-1498a15a5609'\''::uuid AND name = '\''Demo Corporation'\'') AS demo_company, (SELECT count(*) FROM employees WHERE company_id = '\''b4375333-b12b-5fca-b984-87864032d3a8'\''::uuid AND environment_id = '\''b93f752e-7b69-5e8b-8f74-1498a15a5609'\''::uuid) AS demo_employees"'
rtk proxy curl --silent --show-error --fail http://127.0.0.1:15501/api/v1/health/ready
rtk proxy curl --silent --show-error --fail http://127.0.0.1:15500/
```

Điều kiện sau deploy: revision `20261020_0010`; PostgreSQL/API/web healthy; kết quả Demo Corporation là `1` và số employee vẫn `3`; volume PostgreSQL giữ đúng tên trên; đúng một container `agent-corporation-runtime-worker` với trạng thái running (worker không có healthcheck riêng); CG01 vẫn strict và blocked nếu proof chưa được thiết lập; không grant, không inference. Xác minh lại demo dashboard bằng Owner/browser sau khi deploy, không reset fixture. Nếu migration hoặc bootstrap fail thì dừng ở logs đã lọc, không chạy `down --volumes`, không thử reset/seeding.

Đây là thủ tục chờ phê duyệt, chưa thực thi. Trước live demo còn cần Owner quyết định riêng về deploy và grant; CG01 strict hiện chưa pass.
