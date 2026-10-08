"""Smoke parser report bằng fixtures tạm; không test sản phẩm/inference."""
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(BASE / 'scripts'))
from validate import check_report

for script in (BASE / 'scripts').glob('*.py'):
    compile(script.read_text(), str(script), 'exec')
print('PASS Python syntax: render.py/validate.py')

meta = '''# Fixture kiểm validator
- Phase: 00
- Test batch: fixture
- Bắt đầu / kết thúc: fixture
- Người/AI kiểm định: fixture
- Yêu cầu/phạm vi được giao: kiểm parser
- Source: fixture
- Môi trường/config/tool versions: tempfile
- Inference: không gọi
- Dependency/quyết định nghiệm thu: không áp dụng cho fixture parser
- Supersedes: không có
- Kết luận kỹ thuật: đạt
- Quyết định Chủ tịch: Chưa có
'''
summary = '''
## Tổng hợp
| clean | 1 |
| need-change | 0 |
| suggestion | 0 |
| pass | 1 |
| fail | 0 |
| blocked | 0 |
| not-run | 0 |
| not-applicable | 0 |
'''
case = '''
## Kết quả từng test
### C01 — fixture
- Nguồn/tiêu chí: parser fixture
- Bắt buộc: có
- Điều kiện/môi trường: tmp
- Bước/lệnh: parser, exit 0
- Kỳ vọng: valid
- Thực tế: valid
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [fixture](evidence.md)
- Xử lý/đề xuất: không
'''
source = meta + summary + case
with tempfile.TemporaryDirectory(prefix='phase-rule-validator-') as tmp:
    root = Path(tmp)
    (root / 'evidence.md').write_text('Fixture parser, không proof sản phẩm.')
    report = root / 'report.md'
    report.write_text(source)
    assert check_report(report, {'C01'}) == 1
    print('PASS validator nhận report hợp lệ có tag/result/evidence')
    blocked = (meta.replace('- Phase: 00', '- Phase: 03').replace('- Kết luận kỹ thuật: đạt', '- Kết luận kỹ thuật: chưa đủ bằng chứng')
               + summary.replace('| clean | 1 |', '| clean | 0 |').replace('| need-change | 0 |', '| need-change | 1 |').replace('| pass | 1 |', '| pass | 0 |').replace('| not-run | 0 |', '| not-run | 1 |')
               + case.replace('- Tag: clean', '- Tag: need-change').replace('- Kết quả: pass', '- Kết quả: not-run')
               + '''
## Gates
| IG03 | PASS | C01 | [proof](evidence.md) |
''')
    bad_cases = [
        ('clean/not-run', source.replace('- Kết quả: pass', '- Kết quả: not-run'), {'C01'}),
        ('thiếu case bắt buộc', source, {'C01', 'C02'}),
        ('NA case bắt buộc', source.replace('- Tag: clean', '- Tag: suggestion').replace('- Kết quả: pass', '- Kết quả: not-applicable'), {'C01'}),
        ('evidence link hỏng', source.replace('(evidence.md)', '(missing.md)'), {'C01'}),
        ('thống kê sai', source.replace('| clean | 1 |', '| clean | 2 |'), {'C01'}),
        ('trùng Tag', source.replace('- Tag: clean', '- Tag: clean\n- Tag: suggestion'), {'C01'}),
        ('thiếu gate IG03', source.replace('- Phase: 00', '- Phase: 03'), {'C01'}),
        ('gate PASS với not-run', blocked, {'C01'}),
    ]
    for label, content, expected in bad_cases:
        report.write_text(content)
        try:
            check_report(report, expected)
        except ValueError:
            print('PASS từ chối: ' + label)
        else:
            raise AssertionError('Accepted invalid report: ' + label)
print('LIMIT: fixtures parser trong tempfile, không kết quả phase/runtime/inference.')
