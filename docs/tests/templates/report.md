# Kiểm định Phase NN — <test_batch_id>

> Mẫu chưa thực thi. Sao chép vào results/phase-NN/<test_batch_id>/report.md; thay toàn bộ placeholder. Không dùng template làm evidence pass.

## Thông tin batch

- Phase: NN
- Test batch: <test_batch_id>
- Vòng: <rNNN; khớp tên batch>
- Bắt đầu / kết thúc: <ISO 8601 +07:00; Asia/Ho_Chi_Minh>
- Người/AI kiểm định: <tên>
- Độc lập với AI triển khai/remake: <agent ID nguồn và agent ID kiểm định; không tự khai nếu không có agent khác>
- Yêu cầu/phạm vi được giao: <nguồn chỉ thị>
- Source: <commit + dirty state, link manifest/hashes>
- Môi trường/config/tool versions: <refs đã lọc, không secrets>
- Inference: <không gọi; hoặc grant_id/version + phase/batch/purpose/limits/expiry/Owner ref>
- Dependency/quyết định nghiệm thu: <links, ảnh hưởng, mismatch>
- Supersedes: <link batch cũ hoặc không có>
- Remake nguồn: <link remake đã thực hiện trước test này hoặc Không có ở vòng đầu>
- Kết luận kỹ thuật: <đạt | cần sửa | chưa đủ bằng chứng>
- Quyết định Chủ tịch: <Chưa có hoặc nguồn quyết định thật; không tự nghiệm thu>

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| <từng criteria trong roadmap/spec, không bỏ gạch đầu dòng> | <Cxx/PNN-xx> | <loại> | <scope> |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | <n> |
| need-change | <n> |
| suggestion | <n> |

| Result | Số test |
| --- | --- |
| pass | <n> |
| fail | <n> |
| blocked | <n> |
| not-run | <n> |
| not-applicable | <n> |

## Kết quả từng test

Sao chép block dưới cho C01–C08, mọi PNN-* và test bổ sung. Xóa dòng hướng dẫn này sau khi điền.

### <ID> — <tên test>

- Nguồn/tiêu chí: <link nguồn + criteria>
- Bắt buộc: <có | không; loại trừ có nguồn chỉ cho case tùy điều kiện>
- Điều kiện/môi trường: <fixtures/roles/config đã lọc>
- Bước/lệnh: <lệnh rtk từ root hoặc thao tác UI, exit code nếu đã chạy>
- Kỳ vọng: <assertion cụ thể>
- Thực tế: <quan sát, không diễn giải thành pass khi chưa chạy>
- Kết quả phản biện: <none | accepted | rejected; accepted cần contract/evidence và case pass>
- Tag: <clean | need-change | suggestion>
- Kết quả: <pass | fail | blocked | not-run | not-applicable>
- Mức độ: <critical | major | minor | info>
- Evidence: <link tương đối tới file/ảnh/log/manifest; blocked có link mô tả trở ngại>
- Xử lý/đề xuất: <cần sửa gì, cần quyền/tooling gì, hoặc cải tiến tùy chọn>

## Integration / release gates

Mỗi gate là một dòng riêng (IG03/IG08/IG12/IG16/IG20 hoặc R1…R8 theo phase). Phase 23 gồm cả 5 IG và 8 R; audit IG dùng test P23-09 và links report upstream còn phù hợp. PASS phải có tests pass và evidence thật đúng loại; FAIL/BLOCKED ảnh hưởng kết luận.

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| <IG/R đúng phase hoặc không có gate riêng> | <verdict> | <IDs> | <links; run thật khi bắt buộc> |

## Cleanup, giới hạn và bàn giao

- Cleanup: <dataset/resource thuộc batch, thao tác/result; không xóa evidence>
- Chưa kiểm chứng: <test IDs, lý do, ảnh hưởng và việc cần để chạy>
- Cần sửa: <issue IDs + severity + bằng chứng + retest>
- Đề xuất tùy chọn: <test IDs, benefit/effort; không che lỗi bắt buộc>
- Bước tiếp theo: <remake trong phase nếu còn need-change giải quyết được; hoặc đạt kỹ thuật/bị chặn/chỉ test và lý do>
- Bàn giao: <report/evidence/artifacts và kết luận kỹ thuật; không tự chuyển phase>
