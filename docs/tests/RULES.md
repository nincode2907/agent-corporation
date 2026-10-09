# Rule code, test và remake theo phase cho AI

## 1. Kích hoạt và nguồn chuẩn

Flow mặc định khi được giao triển khai, test hoặc remake một phase: **code theo phase → test và ghi results → remake theo results và ghi remakes → test lại và ghi results → tiếp tục nếu còn need-change**. Mọi bước nằm trong cùng phase được giao; không tự chuyển phase. Yêu cầu chỉ viết/cập nhật rule không kích hoạt vòng sửa code sản phẩm.

Trước khi code và trước mỗi vòng test/remake, AI đọc rule này, checklist đúng phase và nguồn hiện tại. Lệnh “test phase NN” mặc định bắt đầu từ test rồi tiếp tục remake/retest trong phạm vi phase; không cần hỏi lại để sửa lỗi thuộc phạm vi đã giao. Nếu người dùng nói rõ “chỉ test”, “không sửa” hoặc yêu cầu dừng, chỉ thực hiện phần được phép. Phase chưa triển khai không tự được triển khai bởi một yêu cầu test để làm cho checklist pass.

Thứ tự đọc: `AGENTS.md` root → rule này → `phases/phase-NN.md` → block NN/dependency trong `docs/master-plan.md` → phần liên quan của `docs/product-spec.md` và ADR → source/diff/tests/evidence hiện tại. Chỉ tải tài liệu cần cho phase. Có thể dùng skill `task-qa-review` cho phương pháp QA; đây là contract riêng của dự án, không cần sao chép skill.

Master-plan chuẩn về phạm vi/trạng thái; spec/ADR chuẩn về hợp đồng/bất biến. Checklist là kế hoạch kiểm chứng. Nếu nguồn lệch nhau, ghi `need-change`, trích vị trí và ảnh hưởng, tiếp tục phần độc lập; không âm thầm chọn trạng thái thuận lợi hay tự sửa quyết định của Chủ tịch. Evidence cũ chỉ chứng minh thời điểm/config cũ, không thay test batch hiện tại.

## 2. Quyền và môi trường

- Chỉ code/test/remake phase được giao và regression của dependency chịu ảnh hưởng. Remake lỗi thuộc phase là phần của flow mặc định; chỉ yêu cầu kiểm định khi người dùng nói rõ không sửa thì không sửa implementation. Không tự chuyển phase, commit/push, tạo công ty thật hoặc thay cấu hình toàn máy. Quyền sửa code không tự cấp inference grant, quyền reset dữ liệu dùng chung hoặc thay quyết định của Chủ tịch.
- Shell luôn qua `rtk`; thiếu trong PATH thì tìm binary có sẵn, không cài global. Không thay port: đọc registry khi cần host port, giữ runtime trong terminal nhìn được log và chỉ báo URL đã kiểm chứng.
- Unit/static/fixture checks không inference có thể chạy trong scope. Trước test ghi DB, reset, kill/restart, migration, restore hoặc fault injection: đọc test/source, xác minh tài nguyên thuộc môi trường kiểm định, dùng dataset riêng có ID và cleanup có scope. Không dừng DB/runtime đang dùng hoặc xoá dữ liệu để thử lỗi nếu chưa có quyền cho thao tác đó; thay bằng môi trường cô lập được phép, nếu chưa có thì ghi blocked và tiếp tục test độc lập.
- Không đọc/in `.env`, auth token, native sessions/transcripts hoặc secrets thật để làm evidence. Chỉ kiểm tra ignore/mode/reference; secret canary là dữ liệu giả. Redact **trước khi lưu** report/log/screenshot; không redirect raw output chứa credential vào thư mục tracked. Nếu không giữ được nội dung, lưu hash/metadata và mô tả cách đối chiếu an toàn.
- Inference mặc định deny. Grant phải do Chủ tịch cấp riêng cho phase + test_batch_id + purpose/cases + model/effort + scope + requests gồm retry/children + concurrency/timeout/limits/basis + expiry. Nghiệm thu, quyền của phiên Codex và grant batch trước không cấp quyền mới. Đợt fail/kết thúc cần grant mới khi chạy lại; late usage chỉ reconcile call cũ. Không thay runtime thật bằng mock để pass gate bắt buộc run thật.
- Đọc contract/source gateway khi đến test adapter. Không sửa/restart/nới quyền gateway chung; health/models không chứng minh entitlement. CG01 không đạt → blocked + gap report; phương án thay đổi cần quyết định riêng. Replay chỉ đọc; unknown side effect không auto retry.

## 3. Vòng code → test → remake → retest

### 3.0. Pipeline tự động và vai trò AI

Chủ tịch giao “chạy Phase NN” một lần rồi theo dõi pipeline. AI điều phối tự bàn giao giữa các vai trò, cập nhật files/HTML sau mỗi bước và tiếp tục vòng tiếp theo; không yêu cầu Chủ tịch tick issue, chuyển file, copy prompt hoặc duyệt từng vòng.

- **AI triển khai/remake:** code phase, nhận report của AI test, sửa hoặc phản biện từng issue và lưu remakes. Không tự duyệt phản biện của mình.
- **AI test độc lập:** một agent khác với AI vừa code/sửa; đọc source và contract trực tiếp, chạy kiểm định, ghi issues vào results, kiểm tra lại cả bản sửa và phản biện. Quyết định giữ/đóng/reopen issue bằng evidence.
- **AI điều phối:** giao việc qua công cụ agent khi có, tuần tự hóa các thao tác ghi cùng source, theo dõi report/remake và gọi AI test cho vòng tiếp theo. Task bàn giao phải chỉ rõ phase, source revision/dirty hashes, round, report nguồn, scope, quyền và vị trí lưu. Các AI dùng cùng contract/ID; không tự mở phase mới.

Khi công cụ agent không khả dụng, ghi rõ thiếu kiểm định độc lập và hoàn thành phần được phép; không giả danh nhiều AI hoặc yêu cầu Chủ tịch thao tác thay giữa các bước. Quyền gọi agent cộng tác cho pipeline này do chỉ thị Chủ tịch cấp; không đồng nghĩa grant gọi model trong runtime sản phẩm. Flow chạy trong phiên được giao, không khẳng định HTML tự khởi chạy agent nền.

### 3.0a. Issue, phản biện và dấu tick do AI cập nhật

- Test xong, AI test ghi từng issue bằng test ID vào report: expected/actual, evidence và hướng xử lý. Report mới nhất và lịch sử remake là nguồn của tab Kiểm thử; dữ liệu localStorage/checkbox cá nhân không quyết định trạng thái issue.
- Remake xong, AI remake ghi `Trạng thái xử lý: changed` và thay đổi/evidence: tab tự hiện **✓ Đã sửa · chờ test lại**. Tick này thể hiện có ghi nhận sửa, chưa phải kết luận pipeline OK.
- Nếu không đồng ý issue, ghi `Trạng thái xử lý: rebutted`, field `Phản biện`, contract/source/evidence và lý do issue sai. Tab hiện **Đã phản biện · chờ AI test xác minh**, không tự tick đóng issue.
- AI test vòng kế tiếp ghi `Kết quả phản biện: accepted` hoặc `rejected` cho case có phản biện (các case khác: `none`). Accepted chỉ khi bằng chứng phù hợp contract và case đạt; tag/result vẫn theo §4. Phản biện không được bỏ criteria bắt buộc hay biến blocked thành pass.
- Test lại đạt → **✓ Đã sửa · test lại đạt**; phản biện được xác minh đạt → **✓ Phản biện được AI test chấp nhận**. Test lại vẫn fail/blocked/not-run → issue mở lại, bỏ tick sửa chưa được chứng minh và chuyển remake tiếp.
- Issue đã đóng vẫn hiển thị trong lịch sử, cùng ghi nhận test/sửa/phản biện và links. Case biến mất khỏi report sau không tự đóng issue. AI render `scripts/render_plan.py` sau mỗi results/remakes cập nhật để Chủ tịch refresh tab theo dõi.
- Pipeline chỉ **OK** khi report hiện tại kết luận `đạt`, gate PASS và mọi issue bắt buộc đã được AI test xác minh; một tick sửa hay phản biện chưa duyệt không đủ. Không cần Chủ tịch tick/xác nhận để AI tiếp tục các vòng; nghiệm thu chính thức vẫn là quyết định riêng.

Tab Kiểm thử luôn hiện một trạng thái pipeline dễ đọc: trước review là **Đã code, chờ review**; report có lỗi chưa remake là **Đã review có lỗi, chờ remake**; đã lưu remake và chờ AI test độc lập là **Đã remake, chờ review**; đủ điều kiện kết thúc kỹ thuật là **Pipeline OK**. Nếu có blocker, hiển thị **Review bị chặn** thay vì che blocker bằng một trong các trạng thái thường. Trạng thái đầu áp dụng khi phase đã được triển khai nhưng chưa có report; phase `Chưa triển khai` hiện **Chưa code**.

### 3.1. Code theo phase

- Đọc scope/dependency/criteria của Phase NN; triển khai đúng phase hoặc tiếp nhận implementation hiện có khi được giao test/remake.
- Xác nhận phiên bản source và thay đổi có sẵn của người dùng; giữ nguyên phần ngoài scope. Không tự làm phase sau để bù dependency chưa có.
- Sau code, chuyển ngay sang test. Code xong hoặc build pass chưa phải phase đạt.

### 3.2. Test và ghi results

1. Ghi phase, test_batch_id, thời gian Asia/Ho_Chi_Minh, người/AI kiểm định, yêu cầu giao việc, revision/commit + dirty diff/hash, config/tool versions, môi trường và quyền/grant ref đã lọc. Không coi commit hash đủ khi worktree dirty. Lưu file list/source hashes của phần được kiểm định.
2. Đọc dependency và quyết định nghiệm thu có nguồn. Ghi các điểm thiếu/khác; kiểm tra phần ảnh hưởng thay vì tin nhãn Hoàn tất. Từ chối phạm vi chưa được giao.
3. Lập danh sách gồm C01–C08 bên dưới, tất cả PNN-* trong checklist, gate đúng phase và case bổ sung từ diff/rủi ro. Ánh xạ **từng** gạch đầu dòng nghiệm thu hiện tại tới test ID; criteria mới chưa có test phải bổ sung. Test plan không chứa tag kết quả sẵn.
4. Chạy happy path và negative/bypass/boundary; thêm race/crash/recovery khi phase có invariant tương ứng. Xác minh ở DB/backend/executor/UI đúng lớp, không coi hidden button/build/lint là proof cho permission hay mobile UX. Ghi lệnh, exit code, observed output và evidence. Chỉ lặp test khi sửa đổi/failure hoặc nghi vấn mới biện minh.
5. Nếu thiếu quyền/grant/dependency/tooling, ghi blocked ở từng case cùng việc cần để chạy; tiếp tục checks độc lập. Nếu chưa thực hiện, ghi not-run. Không tự tạo mock result hay cho clean vì test “có trong source”.
6. Lưu report/evidence vào `results` **trước khi remake**; kiểm tra đủ IDs, tags, links và kết luận. Report là snapshot của source lúc test, không được sửa lại để biến test cũ thành pass sau khi code thay đổi.
7. Đọc mọi `need-change` trong report vừa lưu, lập danh sách xử lý theo test ID và mức độ. Nếu còn việc giải quyết được trong scope/quyền hiện tại thì chuyển ngay sang remake; nếu đạt thì bàn giao. Không coi báo cáo kết quả là kết thúc flow khi còn lỗi có thể xử lý.

### 3.3. Remake theo results và ghi remakes

1. Tạo batch remake cùng số vòng với report nguồn, dùng [mẫu remake](templates/remake.md). Link chính xác report nguồn và từng test ID cần xử lý; ưu tiên lỗi critical/major rồi minor, bao gồm cả thiếu test/evidence bắt buộc.
2. Với mỗi `need-change`, đọc expected/actual/evidence và source hiện tại; xác định nguyên nhân trước sửa. `fail` cần sửa hành vi; `blocked/not-run` cần giải quyết điều kiện hoặc bổ sung kiểm chứng, không mặc định là bug sản phẩm.
3. Sửa code, test, tài liệu hoặc cách lưu evidence thuộc phase đã giao. Nếu thiếu screenshot, tìm cách lưu ảnh và thực hiện lại UI check; không chỉ ghi “chưa lưu” rồi dừng khi vẫn có công cụ hợp lệ để làm. Không hạ tag, loại criteria hay viết mock để né proof bắt buộc.
4. Ghi vào `remake.md`: test ID nguồn, nguyên nhân, thay đổi thực tế/file refs hoặc phản biện có evidence, kiểm tra đã chạy, source trước/sau và phần còn thiếu. Trạng thái xử lý là `changed`, `rebutted`, `blocked` hoặc `no-change`; đây không phải ba tag test và không tự đóng finding.
5. Sau khi thay đổi, chuyển sang retest ở vòng kế tiếp. Không chờ xác nhận giữa các vòng sửa trong phạm vi đã giao. `suggestion` là cải tiến tùy chọn: ghi lựa chọn làm/để lại, không bắt buộc sửa để đạt phase.

### 3.4. Test lại và tiếp tục

- Tăng số vòng, tạo report mới trong `results`; link `Supersedes` tới report trước và `Remake nguồn` tới batch remake vừa thực hiện. Giữ nguyên test ID cho cùng criteria; nếu thêm biến thể/rủi ro thì thêm case, không đổi nghĩa ID cũ.
- Test lại ca lỗi, happy path và regression chịu ảnh hưởng; kiểm đủ C01–C08, checklist và gate. Case bắt buộc chưa thực hiện ở vòng mới không được copy tag `clean` từ report trước. Có thể link evidence cũ làm ngữ cảnh nhưng phải ghi rõ chưa rerun.
- Finding chỉ đóng khi retest có evidence `clean/pass` hoặc `suggestion/pass` hợp lệ. “Đã sửa” trong remake, build pass hay assertion có trong source chưa chứng minh finding đã hết.
- Nếu report mới còn `need-change` có thể giải quyết, tiếp tục remake cùng số vòng của report mới rồi retest vòng tiếp theo. Không tạo batch mới chỉ để lặp cùng lệnh trên source/điều kiện không đổi mà không có lý do.

### 3.5. Khi nào dừng

- **Đạt kỹ thuật:** tất cả test bắt buộc pass, gate áp dụng PASS, evidence đầy đủ và không còn `need-change`; bàn giao report cuối và các suggestion chưa làm cho Chủ tịch nghiệm thu.
- **Bị chặn:** sau khi hoàn thành phần độc lập, việc còn lại thực sự cần grant/quyền, dependency thuộc phase khác, công cụ không khả dụng hoặc quyết định Chủ tịch. Ghi blocker, test IDs, bằng chứng đã thử và điều kiện để tiếp tục trong report/remake; không quay vòng vô hạn, không tự làm phase khác. Khi điều kiện được giải quyết, tiếp tục vòng mới.
- **Chỉ test hoặc người dùng dừng:** lưu kết quả hiện tại và danh sách còn lại theo đúng chỉ thị.

Kết luận kỹ thuật không thay quyết định nghiệm thu. Chỉ cập nhật trạng thái chính thức khi có quyết định rõ trong phạm vi được giao; Markdown trước, render HTML đúng script của dự án.

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

## 7. Quy ước tên thư mục, file và liên kết vòng

Phase dùng hai chữ số `phase-NN`; vòng dùng ít nhất ba chữ số `r001`, `r002`… và tăng liên tục trong phase. Test đầu tiên theo flow mới là `r001`; remake của report `r001` cũng mang `r001`; test sau remake là `r002`. Tiếp tục từ số vòng lớn nhất đã lưu, không tự quay về `r001` khi đổi phiên AI. Batch cũ không có số vòng là legacy; giữ nguyên tên và có thể link làm report nguồn của `r001`.

- `test_batch_id = YYYYMMDDTHHMMSS+0700-rNNN-test`
- `remake_batch_id = YYYYMMDDTHHMMSS+0700-rNNN-remake`

Timestamp lấy lúc bắt đầu thao tác thực theo Asia/Ho_Chi_Minh; không đặt timestamp giả hoặc dự đoán. ID ASCII, không secret. Chốt ID một lần trước khi tạo folder rồi dùng cùng giá trị trong đường dẫn, report, links và lệnh validator. Nếu trùng tên, thêm suffix `-02`, `-03` thay vì ghi đè. Số vòng xác định thứ tự logic; timestamp xác định đợt thực thi.

```text
docs/tests/results/phase-NN/
  README.md                         # Sổ vòng: report → remake → retest
  20261008T170000+0700-r001-test/
    report.md
    evidence/
      source-manifest.json
      commands.md
      PNN-01-observation.md
      PNN-05-desktop.png
  20261008T173000+0700-r002-test/
    report.md
    evidence/...

docs/remakes/phase-NN/
  20261008T171500+0700-r001-remake/
    remake.md
    evidence/
      source-manifest.json
      commands.md
      PNN-01-change.md
```

`report.md`, `remake.md`, `source-manifest.json`, `commands.md` là tên cố định trong mỗi batch. Evidence riêng case dùng `<test_id>-<nội-dung>.<ext>`; nhiều ảnh/biến thể thêm hậu tố như `P04-05-mobile-390.png`, `P03-06-concurrent-01.txt`. File dùng chung ghi test IDs được chứng minh. Không tạo file trống hay placeholder để làm validator pass.

Mỗi report mới ghi `Vòng`, `Supersedes`, `Remake nguồn`; `r001` chưa có nguồn ghi “Không có”, hoặc link report legacy nếu đang retest việc đã làm. Mỗi remake ghi `Vòng`, `Report nguồn`; report retest mới link lại remake đã thực hiện. Không thêm forward links vào report/remake đã chốt; ghi liên kết kế tiếp vào `results/phase-NN/README.md`.

Sổ vòng `results/phase-NN/README.md` có các cột: Vòng, Report test, Kết luận, Remake, Report retest, Trạng thái vòng (`needs-remake`, `needs-retest`, `blocked`, `done`). Cập nhật sau mỗi bước; chỉ link file thực sự tồn tại, chưa có thì ghi “Chưa tạo”. Report/remake đã chốt giữ nguyên lịch sử; sửa sai bằng file đính chính riêng và ghi ở sổ vòng. Không rename hay chuyển các report/remake legacy.

Dùng [mẫu report](templates/report.md) và [mẫu remake](templates/remake.md); hướng dẫn thư mục sửa tại [docs/remakes/README.md](../remakes/README.md). Report link tới evidence bàn giao `docs/evidence/` khi phù hợp, không thay thế lịch sử ở đó. Không lưu DB dump, secrets, gateway transcripts hoặc artifact nhạy cảm vào tracked files. Báo cáo nhỏ/logs không cần HTML riêng; `index.html` là bản trực quan của flow/rule/checklist.
