# Commands và kết quả r004

Tất cả shell qua `rtk proxy`. macOS15.7.7 arm64, Python3.14.8, uv0.12.23, Node24.21.0/npm11.19.0. Source HEAD f74320e2ff20516ec93fbfe3413cfb953695b51d, tracked source clean trước test; không dùng .env, secret Owner/gateway thật, native rollout hoặc transcript.

## PostgreSQL cô lập / C07 / P05-04 / P05-05

Đọc registry block15500–15599; `rtk proxy lsof -nP -iTCP:15500-15599 -sTCP:LISTEN`:15510 sharedPG và15501 sharedAPI;15591 trống. Reserve15591 cho batch. `rtk proxy docker run --name ac-p05-r004-pg --label qa.batch=phase05-r004 --rm -d -e POSTGRES_USER=qa_owner -e POSTGRES_PASSWORD=<synthetic-fixture-only> -e POSTGRES_DB=qa_p05 -p 127.0.0.1:15591:5432 postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` exit0. Không host volume. Credential trong hai script fixture đính kèm là canary tự tạo cho container này, không secret runtime.

`rtk proxy uv run --project apps/api python /tmp/ac-p05-r004-run.py` exit0. Bản tái lập script: [P05-api-fixture.py](P05-api-fixture.py). Monkeypatch Settings(_env_file=None), upgrade Alembic0001→0007 trên disposable DB; app role NOSUPERUSER/NOBYPASSRLS. Pytest gateway6 +Owner auth11 +runtime unit26 +runtime persistence10:

```text
Migration isolated PostgreSQL: head 20261009_0007
53 passed, 1 warning in 4.49s
```

Warning chỉ Starlette TestClient/httpx deprecation, không lỗi hành vi. Các runtime tests dùng transport fake, không chạy worker CLI/gateway model. Persistence tests xác minh 429 requeue bounded, backoff chưa đến hạn không reserve; lần retry giữ model, đạt cap thành failed; unknown/lease expired không replay; RLS/race/snapshot và rollback. Các scope fixture do tests tạo đã cleanup; profile fixture còn lại bị xóa cùng container.

`rtk proxy uv run --project apps/api python /tmp/ac-p05-r004-extra.py` exit0; [script tái lập](P05-profile-fixture.py). Kết quả [profile](P05-03-profile.md). Live probe chỉ GEThealth/models, available/7IDs/entitlementfalse.

`rtk proxy docker stop ac-p05-r004-pg` exit0, output `ac-p05-r004-pg`; --rm xóa container và DB disposable. Không stop/write/migrate DB15510, không restart API15501/gateway15600.

## Web và UI

AI điều phối chạy `rtk proxy npm run --prefix apps/web lint` exit0 và `rtk proxy npm run --prefix apps/web build` exit0: TypeScript+Vite8.3.3,19modules, JS285.89kB. [UI observation](P05-ui-observation.md) ghi browser actions và fake gateway error scenarios. Reviewer độc lập đã đọc đối chiếu evidence và source.

## Harness corrections

Một lệnh `uv run ... python -c` đầu tiên thiếu sys.path nên ModuleNotFoundError; đã thêm apps/api/src, không lỗi sản phẩm. Một đường dẫn catalog giả định sai model-catalog.json được sửa sau đọc catalog.ts sang data/models.json. Không tính hai lỗi harness này là kết quả test sản phẩm.
