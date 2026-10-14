# R005 — Commands và execution hiện tại

## Môi trường và source

Đọc lại RULES, checklist05, remake r004/source/tests. Năm after-hashes trong remake khớp source hiện tại; [manifest](source-manifest.json). HEADf74320e2ff20516ec93fbfe3413cfb953695b51d; source dirty do remake đã chốt. Shell luôn rtk proxy. Python3.14.8/uv0.12.23, PostgreSQL18.6 pinned digest; Node24.21.0/npm11.19.0. Không đọc .env/secret thật hoặc native transcripts.

## DB cô lập và focused regression

Registry block15500–15599 đã đọc. `rtk proxy lsof -nP -iTCP:15500-15599 -sTCP:LISTEN` cho shared15501/15510 và QA15500/15590/15592;15591 trống. Reserve lại15591 cho batch, `rtk proxy docker run --name ac-p05-r005-pg --label qa.batch=phase05-r005 --rm -d -e POSTGRES_USER=qa_owner -e POSTGRES_PASSWORD=<synthetic-fixture-only> -e POSTGRES_DB=qa_p05 -p 127.0.0.1:15591:5432 postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` exit0. Không volume.

`rtk proxy uv run --project apps/api python /tmp/ac-p05-r004-run.py` exit0. Script fixture tái sử dụng hành vi Settings(_env_file=None), migration và scoped test list, không tái dùng kết quả r004: [bản sao script](P05-api-fixture.py). Upgrade database mới0001→0007. Test list: test_codex_gateway.py, test_owner_auth.py, test_phase06_runtime.py, test_phase06_runtime_persistence.py. Suite nay có15regressions mới sau remake:

```text
Migration isolated PostgreSQL: head 20261009_0007
68 passed, 1 warning in 3.17s
```

10 persistence tests chạy thật trong DB riêng, không skip: queue429 bounded/retry limit/backoff, unchanged model/no fallback, unknown crash/recovery fencing, rollback, RLS, snapshots, grants và late usage. Fake transport, không inference. Warning TestClient/httpx deprecation như trước, không lỗi hành vi.

## Original repro và persisted Owner API

`rtk proxy uv run --project apps/api python /tmp/ac-p05-r005-extra.py` exit0, [script đầy đủ](P05-profile-fixture.py). Credential trong script là canary tự tạo của DB container này, không credential thật. [Kết quả](P05-03-profile.md). Original invalid UTF8 repro hiện GETprobe200/contract_mismatch. Metadata thật chỉGET/v1/models +GET/api/models, khôngPOST/session.

## Cleanup

`rtk proxy docker stop ac-p05-r005-pg` exit0/outputac-p05-r005-pg; --rm xóa DB/container disposable, không volume. Canary secret tạm xóa khi context kết thúc. Shared15501/15510/15600 không restart/write/change.

`rtk proxy git diff --check` exit0. Browser/lint/build cho source mới: [UI evidence](P05-ui-observation.md), do AI điều phối thực thi và reviewer đọc đối chiếu; không coi build là CG01 proof.
