# Rule kiểm định phase cho AI

## 1. Kích hoạt và nguồn chuẩn

Sau khi triển khai xong phase được giao, AI phải đọc rule này và checklist đúng phase, kiểm định rồi lưu kết quả trước báo cáo bàn giao. Yêu cầu kiểm định lại cũng dùng workflow này. Tạo bộ rule không có nghĩa chạy tất cả phase. Phase chưa triển khai không tự được triển khai để hoàn thành checklist.

Thứ tự đọc: `AGENTS.md` root → rule này → `phases/phase-NN.md` → block NN/dependency trong `docs/master-plan.md` → phần liên quan của `docs/product-spec.md` và ADR → source/diff/tests/evidence hiện tại. Chỉ tải tài liệu cần cho phase. Có thể dùng skill `task-qa-review` cho phương pháp QA; đây là contract riêng của dự án, không cần sao chép skill.

Master-plan chuẩn về phạm vi/trạng thái; spec/ADR chuẩn về hợp đồng/bất biến. Checklist là kế hoạch kiểm chứng. Nếu nguồn lệch nhau, ghi `need-change`, trích vị trí và ảnh hưởng, tiếp tục phần độc lập; không âm thầm chọn trạng thái thuận lợi hay tự sửa quyết định của Chủ tịch. Evidence cũ chỉ chứng minh thời điểm/config cũ, không thay test batch hiện tại.

## 2. Quyền và môi trường

- Chỉ kiểm định phase được giao và regression của dependency chịu ảnh hưởng. Không tự chuyển phase, commit/push, sửa implementation trong lượt chỉ yêu cầu kiểm định, tạo công ty thật hoặc thay cấu hình toàn máy.
- Shell luôn qua `rtk`; thiếu trong PATH thì tìm binary có sẵn, không cài global. Không thay port: đọc registry khi cần host port, giữ runtime trong terminal nhìn được log và chỉ báo URL đã kiểm chứng.
- Unit/static/fixture checks không inference có thể chạy trong scope. Trước test ghi DB, reset, kill/restart, migration, restore hoặc fault injection: đọc test/source, xác minh tài nguyên thuộc môi trường kiểm định, dùng dataset riêng có ID và cleanup có scope. Không dừng DB/runtime đang dùng hoặc xoá dữ liệu để thử lỗi nếu chưa có quyền cho thao tác đó; thay bằng môi trường cô lập được phép, nếu chưa có thì ghi blocked và tiếp tục test độc lập.
- Không đọc/in `.env`, auth token, native sessions/transcripts hoặc secrets thật để làm evidence. Chỉ kiểm tra ignore/mode/reference; secret canary là dữ liệu giả. Redact **trước khi lưu** report/log/screenshot; không redirect raw output chứa credential vào thư mục tracked. Nếu không giữ được nội dung, lưu hash/metadata và mô tả cách đối chiếu an toàn.
- Inference mặc định deny. Grant phải do Chủ tịch cấp riêng cho phase + test_batch_id + purpose/cases + model/effort + scope + requests gồm retry/children + concurrency/timeout/limits/basis + expiry. Nghiệm thu, quyền của phiên Codex và grant batch trước không cấp quyền mới. Đợt fail/kết thúc cần grant mới khi chạy lại; late usage chỉ reconcile call cũ. Không thay runtime thật bằng mock để pass gate bắt buộc run thật.
- Đọc contract/source gateway khi đến test adapter. Không sửa/restart/nới quyền gateway chung; health/models không chứng minh entitlement. CG01 không đạt → blocked + gap report; phương án thay đổi cần quyết định riêng. Replay chỉ đọc; unknown side effect không auto retry.

## 3. Quy trình một batch

1. Ghi phase, test_batch_id, thời gian Asia/Ho_Chi_Minh, người/AI kiểm định, yêu cầu giao việc, revision/commit + dirty diff/hash, config/tool versions, môi trường và quyền/grant ref đã lọc. Không coi commit hash đủ khi worktree dirty. Lưu file list/source hashes của phần được kiểm định.
2. Đọc dependency và quyết định nghiệm thu có nguồn. Ghi các điểm thiếu/khác; kiểm tra phần ảnh hưởng thay vì tin nhãn Hoàn tất. Từ chối phạm vi chưa được giao.
3. Lập danh sách gồm C01–C08 bên dưới, tất cả PNN-* trong checklist, gate đúng phase và case bổ sung từ diff/rủi ro. Ánh xạ **từng** gạch đầu dòng nghiệm thu hiện tại tới test ID; criteria mới chưa có test phải bổ sung. Test plan không chứa tag kết quả sẵn.
4. Chạy happy path và negative/bypass/boundary; thêm race/crash/recovery khi phase có invariant tương ứng. Xác minh ở DB/backend/executor/UI đúng lớp, không coi hidden button/build/lint là proof cho permission hay mobile UX. Ghi lệnh, exit code, observed output và evidence. Chỉ lặp test khi sửa đổi/failure hoặc nghi vấn mới biện minh.
5. Nếu thiếu quyền/grant/dependency/tooling, ghi blocked ở từng case cùng việc cần để chạy; tiếp tục checks độc lập. Nếu chưa thực hiện, ghi not-run. Không tự tạo mock result hay cho clean vì test “có trong source”.
6. Khi được giao sửa: giữ report batch trước, sửa trong phạm vi, retest ca lỗi và regression liên quan ở batch mới; liên kết supersedes và evidence mới. Không xóa findings cũ hoặc tái dùng grant đã kết thúc.
7. Lưu report/evidence, kiểm tra completeness và tags, kết luận kỹ thuật + giới hạn, bàn giao cho Chủ tịch rồi dừng. Chỉ cập nhật trạng thái chính thức khi có quyết định nghiệm thu rõ trong phạm vi được giao; Markdown trước, render HTML đúng script của dự án.

## 4. Ba tag và kết quả thực thi

Mỗi test có **đúng một** tag và một kết quả riêng:

| Tag | Kết quả cho phép | Điều kiện |
| --- | --- | --- |
| `clean` | `pass` | Đã thực hiện, đủ evidence, đạt mọi kỳ vọng của case, không thiếu kiểm chứng bắt buộc |
| `need-change` | `fail`, `blocked`, `not-run` | Sai hành vi hoặc chưa chứng minh; ghi rõ loại, ảnh hưởng và bước xử lý |
| `suggestion` | `pass`; `not-applicable` cho case tùy điều kiện | Criteria đạt và cải tiến không bắt buộc; loại trừ phải dẫn nguồn/điều kiện, không được loại criteria bắt buộc |

`need-change + blocked/not-run` là khoảng trống kiểm chứng, không tự coi là bug đã xác nhận. Không dùng suggestion để hạ lỗi bảo mật, isolation, budget, recovery hoặc tiêu chí nghiệm thu thiếu evidence. Một test đạt kèm cải tiến tùy chọn có tag suggestion và vẫn phải có evidence pass. Mức độ riêng: `critical` (escape/leak/data loss, bypass quyền hoặc dispatch trái grant), `major` (sai criteria/invariant hoặc thiếu proof bắt buộc), `minor` (lỗi nhỏ), `info` (đạt/đề xuất). Đánh giá theo ảnh hưởng thực tế; nêu mức độ tạm thời nếu chưa kiểm chứng.

Mỗi case ghi ID, nguồn/tiêu chí, bắt buộc hay tùy điều kiện, điều kiện/môi trường, bước/lệnh, expected, actual, tag, result, severity, evidence và hướng xử lý/đề xuất. Evidence phải đủ tái kiểm tra; link tồn tại nhưng nội dung không chứng minh criteria vẫn không đủ.

## 5. Kiểm tra chung cho mọi phase

| ID | Kiểm tra | Bước và kỳ vọng | Evidence |
| --- | --- | --- | --- |
| C01 | Phạm vi và diff | Đối chiếu yêu cầu, file list/diff, roadmap; không thêm phase/feature ngoài quyền, giữ user changes | Yêu cầu + commit/dirty file list + source hashes |
| C02 | Dependency và nguồn quyết định | Đọc dependency/evidence, đối chiếu status summary/detail/ADR và nguồn nghiệm thu; ghi mismatch | Links/đoạn nguồn + kết luận, không dựa vào checkbox |
| C03 | Đủ criteria và demo | Mapping mọi criteria hiện tại → case; demo đúng loại đặc tả/fixture/runtime, output mở được | Ma trận criteria + artifact/demo refs |
| C04 | Không thực thi âm thầm | Kiểm tra đường mở trang/health/seed/replay có trong phase không dispatch model/tool trái scope; Phase 00 kiểm source script | Source trace + call counter/spy hoặc network evidence theo lớp; không chạy model để thử quyền chưa có |
| C05 | Scope và dữ liệu nhạy cảm | Đọc boundary, dùng canary nếu có persistence/log/UI; không secret thật/cross-scope ngoài quyền | Negative tests hoặc review nguồn đặc tả ở 00; logs đã lọc |
| C06 | Tài liệu và bản nhìn | Kiểm source/links/commands/HTML tương ứng, lang vi/favicon; report không nâng trạng thái | Validator/render consistency hoặc đối chiếu nguồn; ghi đúng phạm vi checks |
| C07 | Regression liên quan | Chọn test dependency bị diff tác động; ghi lựa chọn, lệnh/exit và giới hạn | Test output + lý do chọn; phase tài liệu kiểm tài liệu, không đòi runtime chưa có |
| C08 | Có thể tái kiểm định | Report đủ IDs/tags, source/config version, expected/actual, evidence, cleanup scoped; không overclaim | Manifest + báo cáo + kiểm tra links/tags |

C01–C08 bắt buộc ở mọi phase; cách kiểm chứng thay đổi theo lớp đã có. Không ghi not-applicable chỉ vì không có runtime ở Phase 00: kiểm các hợp đồng và script tài liệu tương ứng, không yêu cầu chức năng phase sau.

## 6. Gate và kết luận

Checklist Phase 03/08/12/16/20 chứa IG tương ứng; Phase 23 chứa R1–R8 và audit đủ IG trước. Báo riêng mỗi gate `PASS`, `FAIL`, `BLOCKED` kèm test IDs/config/batch/grant/evidence. Gate yêu cầu run thật không được PASS từ static/fixture. Báo cáo cũ được đối chiếu version/scope, không tự coi còn hợp lệ sau thay đổi ảnh hưởng.

Kết luận kỹ thuật của phase:

- `đạt`: mọi test bắt buộc pass và gate PASS, evidence đầy đủ; suggestions không che thiếu criteria.
- `cần sửa`: có test bắt buộc fail hoặc gate FAIL, dù còn test chưa chạy.
- `chưa đủ bằng chứng`: không có fail bắt buộc nhưng còn blocked/not-run, dependency không rõ hoặc gate BLOCKED.

Ưu tiên fail → chưa đủ bằng chứng → đạt. Kết luận không phải trạng thái master-plan, không mở phase tiếp và không cấp release/inference permission. Quyết định Chủ tịch trong report để “Chưa có” nếu không có bằng chứng rõ. Không tự nghiệm thu test bằng thời gian chờ.

## 7. Quy ước lưu

`test_batch_id = YYYYMMDDTHHMMSS+0700-<mục-đích>` (ASCII, tên ngắn, không secret), ví dụ `20261008T143000+0700-persistence`. Timestamp lấy lúc chạy thực theo Asia/Ho_Chi_Minh; nếu trùng thêm suffix. Mỗi batch là thư mục mới:

```text
docs/tests/results/phase-NN/<test_batch_id>/
  report.md
  evidence/
    source-manifest.json
    commands.md
    ... logs đã lọc, ảnh, manifests, receipts ...
```

Dùng [mẫu report](templates/report.md). Report link tới evidence bàn giao `docs/evidence/` nếu thích hợp, không thay thế lịch sử ở đó. Không lưu DB dump, secrets, gateway transcripts hoặc artifact nhạy cảm vào thư mục tracked. Ghi metadata/hash/reference đã authorized. Báo cáo nhỏ và logs không cần HTML riêng; `index.html` là bản trực quan của bộ rule/checklist.
