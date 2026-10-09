# Các vòng remake theo kết quả test

AI đọc [rule code/test/remake](../tests/RULES.md) và report results nguồn trước khi sửa. Remake ghi thay đổi **đã thực hiện**, nguyên nhân, test IDs và việc cần retest. Kết quả test sau sửa vẫn được ghi trong `docs/tests/results/`, không ghi pass thay cho results ở đây.

AI remake khác với AI test và có thể ghi phản biện có contract/evidence (`rebutted`). AI test độc lập xác minh lại và ghi accepted/rejected trong results. Tab tự tick bản sửa đã ghi nhưng ghi rõ đang chờ retest; chỉ đóng issue sau kiểm định đạt. Chủ tịch không phải tick hoặc bàn giao prompt giữa các AI.

Tên batch: `YYYYMMDDTHHMMSS+0700-rNNN-remake`. Cùng số vòng với report nguồn; test sau sửa tăng vòng. Dùng [mẫu remake](../tests/templates/remake.md).

```text
docs/remakes/phase-04/20261008T171500+0700-r001-remake/
  remake.md
  evidence/
    source-manifest.json
    commands.md
    P04-08-change.md
```

`remake.md` link report nguồn và từng finding. Sổ vòng ở `docs/tests/results/phase-NN/README.md` link report → remake → retest, ghi trạng thái còn lại. Không tự sửa report cũ, đổi tag cũ hoặc chốt nghiệm thu.

Nếu còn need-change có thể giải quyết trong scope, AI tiếp tục remake/retest. Nếu cần grant, quyết định hay dependency ngoài scope, lưu blocker và điều kiện tiếp tục. Suggestions không chặn đạt kỹ thuật.

File cũ như `phase-01-followup.md` là legacy; giữ nguyên vị trí và lịch sử, link khi cần, không tự rename.
