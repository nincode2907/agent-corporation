# Sổ vòng kiểm định Phase 05

| Vòng | Report test | Kết luận | Remake | Report retest | Trạng thái vòng |
| --- | --- | --- | --- | --- | --- |
| r001 | [20261008T165432+0700-r001-test](20261008T165432+0700-r001-test/report.md) | cần sửa | [20261008T165817+0700-r001-remake](../../../remakes/phase-05/20261008T165817+0700-r001-remake/remake.md) | [20261008T165952+0700-r002-test](20261008T165952+0700-r002-test/report.md) | blocked |
| r002 | [20261008T165952+0700-r002-test](20261008T165952+0700-r002-test/report.md) | chưa đủ bằng chứng | [20261009T110817+0700-r002-remake](../../../remakes/phase-05/20261009T110817+0700-r002-remake/remake.md) | [20261009T111044+0700-r003-test](20261009T111044+0700-r003-test/report.md) | blocked |
| r003 | [20261009T111044+0700-r003-test](20261009T111044+0700-r003-test/report.md) | Report lịch sử trước Owner/runtime; được r004 kiểm tra lại source mới | Không tạo remake r003 | [r004](20261014T144929+0700-r004-test/report.md) | done |
| r004 | [20261014T144929+0700-r004-test](20261014T144929+0700-r004-test/report.md) | 12 pass,2 fail,1 blocked; gateway/Owner/queue đã kiểm được | [remake r004](../../../remakes/phase-05/20261014T145852+0700-r004-remake/remake.md) | [r005](20261014T150201+0700-r005-test/report.md) | blocked |
| r005 | [20261014T150201+0700-r005-test](20261014T150201+0700-r005-test/report.md) | 14 clean/pass, 0 fail; P05-02/P05-03 đã xác minh sửa; còn P05-06 blocked | Không sửa tiếp: cần evidence/quyết định CG01 | Chưa tạo | blocked |

Ngày 14/10/2026: vòng kiểm định độc lập r004 → remake r004 → retest độc lập r005 đã hoàn tất. Hai lỗi encoding/model-effort được xác minh đã sửa; gateway live, Owner profile/auth và queue 429 đã có evidence mới. Pipeline hiện chỉ bị chặn bởi CG01 `missing_or_invalid_proof`; cần bằng chứng isolation/privacy-retention/cancellation hợp lệ trước khi review gate lại. Không tạo batch lặp với điều kiện chưa đổi. Không inference; Phase 05 vẫn Chờ nghiệm thu.
