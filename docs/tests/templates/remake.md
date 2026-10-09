# Remake Phase NN — <remake_batch_id>

> Mẫu chưa thực thi. Sao chép vào docs/remakes/phase-NN/<remake_batch_id>/remake.md; thay placeholder. Không coi kế hoạch sửa là thay đổi đã làm hoặc evidence pass.

## Thông tin vòng sửa

- Phase: NN
- Remake batch: <remake_batch_id>
- Người/AI remake: <agent ID/tên; khác AI test nguồn>
- Vòng: <rNNN; cùng số vòng với report nguồn>
- Report nguồn: <link report results thực sự tồn tại>
- Bắt đầu / kết thúc: <ISO 8601 +07:00; Asia/Ho_Chi_Minh>
- Phạm vi/quyền: <phase được giao, giới hạn, nguồn chỉ thị>
- Source trước/sau: <commit, dirty diff, file hashes; link evidence/source-manifest.json>
- Inference: <không gọi hoặc grant riêng; không kế thừa grant report nguồn>
- Kết luận vòng sửa: <đã thay đổi và cần retest | bị chặn | không thay đổi, nêu lý do>

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| <ID + link case trong report> | <root cause hoặc gap> | <đã sửa gì/phản biện hoặc chưa sửa vì sao> | <changed / rebutted / blocked / no-change> | <original case + happy path + regression> |

Bao phủ mọi need-change của report nguồn. Suggestions ghi rõ làm/để lại. Không dùng changed để thay tag clean của test; finding chỉ đóng bằng results retest.

## Chi tiết từng finding

### <test_id> — <tên finding>

- Expected/actual nguồn: <tóm tắt và link evidence>
- Nguyên nhân: <có bằng chứng; phân biệt bug và thiếu kiểm chứng>
- Trạng thái xử lý: <changed | rebutted | blocked | no-change; khớp mapping>
- Thay đổi: <file refs/diff thực tế; không mô tả kế hoạch như đã làm>
- Phản biện: <contract/source/evidence và lý do issue không đúng; hoặc Không có>
- Kiểm tra trong lúc sửa: <lệnh, exit code, output và links; không thay report retest>
- Còn thiếu/blocker: <điều kiện để tiếp tục; hoặc Không có>
- Retest cần chạy: <bước và postcondition cụ thể>

## Cleanup và bước tiếp theo

- Cleanup: <test dataset/resources, scope và outcome>
- Evidence: <source-manifest.json, commands.md, change notes đã lọc; links tồn tại>
- Retest tiếp theo: <rNNN kế tiếp; tạo results batch mới khi thực sự bắt đầu test>
- Blocker/giới hạn: <nếu có; không tự mở phase khác>
- Sổ vòng: <link results/phase-NN/README.md cập nhật liên kết retest sau khi file tồn tại>

Giữ remake đã chốt như lịch sử. Không điền report retest giả hoặc tuyên bố finding đóng trước test.
