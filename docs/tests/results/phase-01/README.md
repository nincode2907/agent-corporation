# Sổ vòng kiểm thử và remake — Phase 01

| Vòng | Report test | Kết luận | Remake | Report retest | Trạng thái vòng |
| --- | --- | --- | --- | --- | --- |
| legacy | [20261008T154512+0700-phase01](20261008T154512+0700-phase01/report.md) | Cần sửa / chưa đủ bằng chứng | [20261009T085800+0700-r001-remake](../../../remakes/phase-01/20261009T085800+0700-r001-remake/remake.md) | [20261009T085957+0700-r002-test](20261009T085957+0700-r002-test/report.md) | needs-retest |
| r003 độc lập | [20261009T091040+0700-r003-test](20261009T091040+0700-r003-test/report.md) | Bị r004 đính chính — P01-01 không được kiểm tra đúng lệnh README | Chưa remake | [r004](20261009T091446+0700-r004-test/report.md) | superseded |
| r004 độc lập | [20261009T091446+0700-r004-test](20261009T091446+0700-r004-test/report.md) | Phát hiện P01-01 fail; C03/P01-02/P01-03 chưa đủ evidence tại vòng đó | [Remake r004](../../../remakes/phase-01/20261009T092011+0700-r004-remake/remake.md) | [r005 độc lập](20261009T092254+0700-r005-test/report.md) | đã remake và retest |
| r005 retest độc lập | [20261009T092254+0700-r005-test](20261009T092254+0700-r005-test/report.md) | Đạt kỹ thuật — 15/15 clean/pass; không còn need-change | Không cần | — | done |

R002 do AI triển khai/remake tự retest, không được tính là kiểm định độc lập. Report r003 trước đó đánh clean P01-01 nhưng chỉ chạy `npm ci` từ `apps/web`; report r004 độc lập tái hiện lỗi `npm ci --prefix apps/web` trong bản sao sạch. Remake r004 đổi README sang `npm --prefix apps/web ci`; r005 độc lập chạy lệnh nguyên văn trên bản sao sạch và retest demo, DB-down, baseline migration trong stack cô lập. Vòng r005 đã hoàn tất theo kết quả kỹ thuật; Phase 01 vẫn `Chờ nghiệm thu`, chưa đánh dấu hoàn tất và chưa mở phase tiếp theo.
