#!/usr/bin/env python3
"""Kiểm cấu trúc tài liệu/report; không đánh giá thay nội dung evidence hoặc test sản phẩm."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from render import BASE, render

ROOT = BASE.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def section(block: str, name: str) -> str:
    marker = f'#### {name}\n'
    require(marker in block, f'Thiếu section {name}')
    return block.split(marker, 1)[1].split('\n#### ', 1)[0].strip()


def contract(block: str) -> str:
    names = ['Phạm vi', 'Demo', 'Nghiệm thu', 'Bàn giao', 'Giới hạn', 'Bằng chứng cần có']
    dep = re.search(r'^- Phụ thuộc: (.+)$', block, re.M)[1]
    return '\n\n'.join(name + '\n' + section(block, name) for name in names) + '\n' + dep


def links(path: Path) -> None:
    for href in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', path.read_text()):
        if re.match(r'^[a-z]+://', href):
            continue
        target = href.split('#', 1)[0]
        if target:
            require((path.parent / target).is_file(), f'Link thiếu tại {path}: {href}')


def field(body: str, name: str) -> str:
    matches = re.findall(rf'^- {re.escape(name)}: (.+)$', body, re.M)
    require(len(matches) == 1 and bool(matches[0].strip()), f'Thiếu/trùng field {name}')
    return matches[0].strip()


def check_report(path: Path, expected: set[str] | None = None) -> int:
    text = path.read_text()
    require('> Mẫu chưa thực thi' not in text and not re.search(r'<[^>\n]+>', text), f'Report còn placeholder: {path}')
    for name in ['Phase', 'Test batch', 'Bắt đầu / kết thúc', 'Người/AI kiểm định', 'Yêu cầu/phạm vi được giao', 'Source', 'Môi trường/config/tool versions', 'Inference', 'Dependency/quyết định nghiệm thu', 'Supersedes', 'Kết luận kỹ thuật', 'Quyết định Chủ tịch']:
        field(text, name)
    case_blocks = list(re.finditer(r'^### ((?:C\d{2}|P\d{2}-\d{2}|[A-Z][A-Z0-9]*-\d+)) — [^\n]+\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S))
    require(bool(case_blocks), f'Report thiếu cases: {path}')
    ids = [m[1] for m in case_blocks]
    require(len(ids) == len(set(ids)), f'Report trùng IDs: {path}')
    if expected is not None:
        require(expected <= set(ids), f'Report thiếu cases: {sorted(expected - set(ids))}')
    results = []
    by_id = {}
    tag_counts = {'clean': 0, 'need-change': 0, 'suggestion': 0}
    result_counts = dict.fromkeys(['pass', 'fail', 'blocked', 'not-run', 'not-applicable'], 0)
    for match in case_blocks:
        ident, body = match[1], match[2]
        for name in ['Nguồn/tiêu chí', 'Bắt buộc', 'Điều kiện/môi trường', 'Bước/lệnh', 'Kỳ vọng', 'Thực tế', 'Tag', 'Kết quả', 'Mức độ', 'Evidence', 'Xử lý/đề xuất']:
            field(body, name)
        tag, result = field(body, 'Tag'), field(body, 'Kết quả')
        allowed = {'clean': {'pass'}, 'need-change': {'fail', 'blocked', 'not-run'}, 'suggestion': {'pass', 'not-applicable'}}
        require(tag in allowed and result in allowed[tag], f'{ident}: tag/result không hợp lệ {tag}/{result}')
        mandatory = field(body, 'Bắt buộc')
        require(mandatory in {'có', 'không'} or mandatory.startswith('không;'), f'{ident}: Bắt buộc phải có/không')
        require(result != 'not-applicable' or mandatory.startswith('không'), f'{ident}: Không loại case bắt buộc')
        if expected is not None and ident in expected:
            require(mandatory == 'có', f'{ident}: Case checklist/C01–C08 là bắt buộc')
        require(field(body, 'Mức độ') in {'critical', 'major', 'minor', 'info'}, f'{ident}: mức độ sai')
        require(bool(re.search(r'\[[^\]]+\]\([^)]+\)', field(body, 'Evidence'))), f'{ident}: cần evidence link')
        results.append((mandatory == 'có', result))
        by_id[ident] = result
        tag_counts[tag] += 1
        result_counts[result] += 1
    for name, count in {**tag_counts, **result_counts}.items():
        summary = re.findall(rf'^\| {re.escape(name)} \| (\d+) \|$', text, re.M)
        require(len(summary) == 1 and int(summary[0]) == count, f'Thống kê {name} sai/thiếu so với cases')
    verdict = field(text, 'Kết luận kỹ thuật')
    predicted = 'cần sửa' if any(m and r == 'fail' for m, r in results) else 'chưa đủ bằng chứng' if any(m and r in {'blocked', 'not-run'} for m, r in results) else 'đạt'
    require(verdict in {'đạt', 'cần sửa', 'chưa đủ bằng chứng'}, f'Report verdict sai: {verdict}')
    require(verdict != 'đạt' or predicted == 'đạt', 'Không được đạt khi test bắt buộc fail/blocked/not-run')
    require(predicted != 'cần sửa' or verdict == 'cần sửa', 'Có fail bắt buộc phải kết luận cần sửa')
    if expected is not None:
        phase = field(text, 'Phase')
        gate_map = {'03': {'IG03'}, '08': {'IG08'}, '12': {'IG12'}, '16': {'IG16'}, '20': {'IG20'}}
        required_gates = gate_map.get(phase, set())
        if phase == '23':
            required_gates = {'IG03', 'IG08', 'IG12', 'IG16', 'IG20'} | {f'R{n}' for n in range(1, 9)}
        rows = re.findall(r'^\| (IG\d{2}|R[1-8]) \| (PASS|FAIL|BLOCKED) \| ([^|]+) \| ([^|]+) \|$', text, re.M)
        gate_ids = [r[0] for r in rows]
        require(len(gate_ids) == len(set(gate_ids)) and required_gates == set(gate_ids), f'Gate thiếu/trùng/sai phase: cần {sorted(required_gates)}')
        for gate, outcome, refs, evidence in rows:
            ids_for_gate = set(re.findall(r'(?:C\d{2}|P\d{2}-\d{2}|[A-Z][A-Z0-9]*-\d+)', refs))
            require(bool(ids_for_gate) and ids_for_gate <= set(ids), f'{gate}: test IDs sai/thiếu')
            require(bool(re.search(r'\[[^\]]+\]\([^)]+\)', evidence)), f'{gate}: thiếu evidence link')
            if outcome == 'PASS':
                require(all(by_id[i] == 'pass' for i in ids_for_gate), f'{gate}: PASS nhưng tests chưa pass')
            elif outcome == 'FAIL':
                require(verdict == 'cần sửa', f'{gate}: FAIL phải kết luận cần sửa')
            else:
                require(verdict != 'đạt', f'{gate}: BLOCKED không được kết luận đạt')
    links(path)
    return len(ids)


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.icon = False
        self.ids: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == 'html':
            self.lang = data.get('lang')
        if tag == 'link' and data.get('rel') == 'icon':
            self.icon = str(data.get('href')).startswith('data:image/svg+xml,')
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'a':
            self.hrefs.append(data.get('href', ''))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, help='Thư mục batch trong docs/tests/results/phase-NN/')
    args = parser.parse_args()
    master = (ROOT / 'docs/master-plan.md').read_text()
    spec = (ROOT / 'docs/product-spec.md').read_text()
    blocks = {m[1]: (m[2], m[3]) for m in re.finditer(r'^### Phase (\d{2}) — ([^\n]+)\n(.*?)(?=^### Phase |^## 8\.|\Z)', master, re.M | re.S)}
    require(set(blocks) == {f'{n:02}' for n in range(24)}, 'Roadmap phải có 24 phase')
    paths = sorted((BASE / 'phases').glob('phase-*.md'))
    require({p.stem for p in paths} == {f'phase-{n:02}' for n in range(24)}, 'Thiếu/trùng checklist phase')
    common = set(re.findall(r'^\| (C\d{2}) \|', (BASE / 'RULES.md').read_text(), re.M))
    require(common == {f'C{n:02}' for n in range(1, 9)}, 'C01–C08 thiếu/trùng')
    expected: dict[str, set[str]] = {}
    total = 0
    for path in paths:
        ident = path.stem[-2:]
        text = path.read_text()
        title, block = blocks[ident]
        require(text.startswith(f'# Kiểm định Phase {ident} — {title}\n'), f'Title lệch roadmap: {ident}')
        digest = hashlib.sha256(contract(block).encode()).hexdigest()
        require(f'- Contract hash: {digest}' in text, f'Checklist {ident} cũ so với contract roadmap; cập nhật mapping/ca test từ nguồn')
        ids = re.findall(r'^\| (P\d{2}-\d{2}) \|', text, re.M)
        require(ids == [f'P{ident}-{n:02}' for n in range(1, len(ids) + 1)] and len(ids) >= 3, f'Test IDs thiếu/trùng/sai phase: {ident}')
        expected[ident] = common | set(ids)
        total += len(ids)
        criteria = [line[2:] for line in section(block, 'Nghiệm thu').splitlines() if line.startswith('- ')]
        mapping = re.findall(r'^\| AC(\d+) \| ([^|]+) \| ([^|]+) \|$', text, re.M)
        require(len(mapping) == len(criteria), f'Thiếu mapping AC: {ident}')
        for n, (number, criterion, refs) in enumerate(mapping, 1):
            require(number == str(n) and criterion.strip() == criteria[n - 1], f'AC lệch source: {ident}/{n}')
            selected = set(re.findall(r'P\d{2}-\d{2}', refs))
            require(bool(selected) and selected <= set(ids), f'AC mapping refs sai: {ident}/{n}')
        for line in text.splitlines():
            if re.match(r'^\| P\d{2}-\d{2} \|', line):
                cells = [c.strip() for c in line.strip('|').split('|')]
                require(len(cells) == 6 and all(cells), f'Test thiếu steps/expected/evidence/source: {line}')
                for number in re.findall(r'Spec §(\d+)', cells[5]):
                    require(re.search(rf'^## {number}\. ', spec, re.M) is not None, f'Spec section ref sai: {ident}/{number}')
    for phase, gate in [('03', 'IG03'), ('08', 'IG08'), ('12', 'IG12'), ('16', 'IG16'), ('20', 'IG20')]:
        require(f'- Gate: {gate}\n' in (BASE / f'phases/phase-{phase}.md').read_text(), f'Thiếu gate {gate}')
    release = (BASE / 'phases/phase-23.md').read_text()
    require(all(f'R{n} ' in release for n in range(1, 9)), 'Phase 23 thiếu R1–R8')
    for path in BASE.rglob('*.md'):
        links(path)
    actual = (BASE / 'index.html').read_text()
    require(actual == render(), 'HTML chưa đồng bộ: chạy docs/tests/scripts/render.py')
    page = Page()
    page.feed(actual)
    require(page.lang == 'vi' and page.icon, 'HTML thiếu lang=vi/favicon')
    require(len(page.ids) == len(set(page.ids)), 'HTML trùng IDs')
    require(all(f'phase-{n:02}' in page.ids for n in range(24)), 'HTML thiếu phase')
    for href in page.hrefs:
        require((BASE / href.split('#', 1)[0]).is_file(), f'HTML link thiếu: {href}')
    print(f'PASS cấu trúc: 24 checklist, {total} test riêng, C01–C08, AC/source refs/hash, IG/R và local links.')
    print('PASS HTML: deterministic/đồng bộ, đủ phase, lang=vi/favicon, IDs/links.')
    reports = [args.batch.resolve() / 'report.md'] if args.batch else sorted((BASE / 'results').glob('phase-*/*/report.md'))
    for path in reports:
        require(path.is_file(), f'Report không tồn tại: {path}')
        relative = path.relative_to(BASE / 'results')
        require(len(relative.parts) == 3 and relative.parts[0] in {f'phase-{n:02}' for n in range(24)}, 'Batch phải nằm trong results/phase-NN/<test_batch_id>/')
        phase = relative.parts[0][-2:]
        require(field(path.read_text(), 'Phase') == phase, 'Phase report khác thư mục')
        require(field(path.read_text(), 'Test batch') == relative.parts[1], 'Batch ID report khác thư mục')
        count = check_report(path, expected[phase])
        print(f'PASS report {relative}: {count} cases có fields/tag/result/evidence links.')
    framework_reports = sorted((BASE / 'results/framework').glob('*/report.md')) if not args.batch else []
    for path in framework_reports:
        require(field(path.read_text(), 'Phase') == 'framework', 'Framework report không được gán kết quả cho phase sản phẩm')
        count = check_report(path)
        print(f'PASS framework report: {count} cases có fields/tag/result/evidence links.')
    print(f'LIMIT: {len(reports)} report phase, {len(framework_reports)} report bộ tài liệu được kiểm cấu trúc; chưa chạy test sản phẩm/inference, chưa đánh giá nội dung evidence hoặc nghiệm thu.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, IndexError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
