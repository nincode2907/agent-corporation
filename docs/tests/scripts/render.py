#!/usr/bin/env python3
"""Dựng trang tra cứu local từ Markdown; không DB, gateway hoặc inference."""
from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def source_digest() -> str:
    digest = hashlib.sha256()
    paths = sorted(p for p in BASE.rglob('*.md') if 'results' not in p.relative_to(BASE).parts)
    for path in paths:
        digest.update(path.relative_to(BASE).as_posix().encode())
        digest.update(b'\0')
        digest.update(path.read_bytes())
        digest.update(b'\0')
    return digest.hexdigest()


def render() -> str:
    cards = []
    total = 0
    for path in sorted((BASE / 'phases').glob('phase-*.md')):
        source = path.read_text()
        title = source.splitlines()[0].removeprefix('# Kiểm định ')
        phase = re.search(r'^- Phase: (\d{2})$', source, re.M)[1]
        deps = re.search(r'^- Dependency từ roadmap: (.+)$', source, re.M)[1]
        gate = re.search(r'^- Gate: (.+)$', source, re.M)[1]
        tests = re.findall(r'^\| (P\d{2}-\d{2}) \| ([^|]+) \|', source, re.M)
        total += len(tests)
        items = ''.join(f'<li><code>{ident}</code> {html.escape(name.strip())}</li>' for ident, name in tests)
        cards.append(f'''<article id="phase-{phase}" class="phase"><span class="number">{phase}</span>
<div><h3><a href="phases/{path.name}">{html.escape(title)}</a></h3>
<p class="muted">Phụ thuộc: {html.escape(deps)} · {len(tests)} test riêng + C01–C08</p>
<p class="gate">{html.escape(gate)}</p><details><summary>Xem các test</summary><ul>{items}</ul></details></div></article>''')
    return f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="source-sha256" content="{source_digest()}">
<title>Bộ kiểm định phase · Agent Corporation</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23162938'/%3E%3Cpath d='m8 16 5 5 11-12' fill='none' stroke='%235de0b0' stroke-width='3'/%3E%3C/svg%3E">
<style>
:root{{color-scheme:light;--ink:#162938;--muted:#516575;--line:#cbd8dc;--paper:#f5f7f5;--green:#166344;--red:#963b39;--blue:#244e9a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,sans-serif}}
main{{max-width:1160px;margin:auto;padding:48px 28px}}a{{color:var(--blue);text-underline-offset:4px}}a:focus-visible,summary:focus-visible{{outline:3px solid #b96b0b;outline-offset:4px}}
.eyebrow{{font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--green);font-weight:750}}h1{{font-size:clamp(2.2rem,5vw,4rem);line-height:1.12;letter-spacing:-.04em;margin:16px 0 24px;max-width:850px}}h2{{font-size:1.65rem;margin:0 0 18px}}h3{{font-size:1.05rem;margin:0}}p{{margin:8px 0 16px}}.lead{{font-size:1.15rem;max-width:800px}}.muted{{color:var(--muted);font-size:.9rem}}
nav{{display:flex;gap:12px 24px;flex-wrap:wrap;margin:24px 0}}section{{margin-top:44px}}.notice{{border-left:4px solid var(--green);padding:14px 20px;background:#e8efe9}}
.metrics{{display:flex;gap:36px;flex-wrap:wrap;border-block:1px solid var(--line);padding:20px 0;margin-top:30px}}.metrics strong{{font-size:2rem;display:block;line-height:1.1}}
.flow{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;padding:0;list-style:none;counter-reset:step}}.flow li{{background:#fff;border-top:3px solid var(--ink);padding:16px;counter-increment:step}}.flow li:before{{content:counter(step,decimal-leading-zero);display:block;color:var(--green);font-weight:750;margin-bottom:12px}}
.tags{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.tag{{padding:18px;background:#fff;border:1px solid var(--line)}}.badge{{font-family:monospace;font-size:1rem;font-weight:750}}.clean{{color:var(--green)}}.change{{color:var(--red)}}.suggestion{{color:var(--blue)}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.phase{{display:flex;gap:18px;padding:22px;background:white;border:1px solid var(--line);min-width:0}}.phase>div{{min-width:0}}.number{{font-size:1.7rem;font-weight:750;color:var(--green)}}.gate{{font-size:.85rem;border-left:2px solid var(--line);padding-left:10px}}summary{{cursor:pointer;color:var(--blue)}}li{{margin-bottom:8px}}code{{font-family:ui-monospace,monospace;font-size:.85em;overflow-wrap:anywhere}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--ink);color:#f3f7fa;padding:20px;border-radius:4px}}.gates{{display:flex;flex-wrap:wrap;gap:10px;padding:0;list-style:none}}.gates li{{padding:10px 16px;background:#e8efe9;border:1px solid var(--line)}}footer{{margin-top:48px;padding-top:20px;border-top:1px solid var(--line)}}
@media(max-width:800px){{.flow{{grid-template-columns:1fr 1fr}}.grid{{grid-template-columns:1fr}}}}@media(max-width:520px){{main{{padding:28px 18px}}.flow,.tags{{grid-template-columns:1fr}}.phase{{padding:16px;gap:12px}}.metrics{{gap:24px}}}}@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto}}}}
</style></head><body><main>
<header><div class="eyebrow">Agent Corporation · Quy trình kiểm định</div><h1>Mỗi phase có bằng chứng để Chủ tịch đánh giá.</h1>
<p class="lead">AI code đúng phase, test và lưu results, remake theo findings rồi test lại. Vòng lặp tiếp tục khi còn need-change giải quyết được trong phạm vi; quyết định nghiệm thu thuộc Chủ tịch.</p>
<nav aria-label="Tài liệu kiểm định"><a href="README.md">Hướng dẫn Markdown</a><a href="RULES.md">Đọc rule đầy đủ</a><a href="templates/report.md">Mẫu report</a><a href="templates/remake.md">Mẫu remake</a><a href="results/README.md">Results</a><a href="../remakes/README.md">Remakes</a><a href="../master-plan.html">Roadmap</a></nav>
<div class="notice">Đây là bộ kế hoạch kiểm định, chưa phải kết quả test sản phẩm. Không tự chuyển phase hoặc gọi inference. Mỗi đợt cần kiểm tra quyền và nguồn hiện tại.</div>
<div class="metrics"><div><strong>24</strong>phase có checklist</div><div><strong>{total}</strong>test riêng theo phase</div><div><strong>8</strong>kiểm tra chung mỗi phase</div><div><strong>3</strong>tag cho từng kết quả</div></div></header>
<section aria-labelledby="flow"><h2 id="flow">Code → test → remake → retest</h2><ol class="flow"><li><b>Code theo phase</b><br>Đọc rule/checklist/nguồn; triển khai đúng scope hoặc tiếp nhận code hiện có.</li><li><b>Test → results</b><br>Lưu report và evidence trước khi sửa; mỗi test có tag/result.</li><li><b>Remake → remakes</b><br>Đọc need-change; sửa trong phase; ghi nguyên nhân và thay đổi theo test ID.</li><li><b>Retest → results mới</b><br>Tăng vòng; link report trước/remake nguồn; kiểm lỗi và regression.</li><li><b>Lặp hoặc bàn giao</b><br>Còn need-change có thể giải quyết thì tiếp tục. Đạt hoặc blocker thật thì báo rõ.</li></ol><p>Yêu cầu “chỉ test/không sửa” dừng sau results. Suggestions tùy chọn; vòng lặp không tự cấp grant/quyền hoặc mở phase tiếp.</p></section>
<section aria-labelledby="tags"><h2 id="tags">Gắn tag sau khi có kết quả</h2><div class="tags"><article class="tag"><span class="badge clean">clean</span><p>Đã chạy, đạt đủ kỳ vọng và có evidence.</p><p class="muted">Result: pass. Không dùng cho test chưa chạy.</p></article><article class="tag"><span class="badge change">need-change</span><p>Sai hành vi hoặc chưa đủ bằng chứng bắt buộc.</p><p class="muted">Result: fail, blocked hoặc not-run. Khoảng trống chưa chứng minh không tự coi là bug.</p></article><article class="tag"><span class="badge suggestion">suggestion</span><p>Đã đạt criteria, có cải tiến tùy chọn.</p><p class="muted">Result: pass; not-applicable chỉ cho case tùy điều kiện có nguồn loại trừ.</p></article></div><p>Tag, kết quả thực thi và mức độ lỗi là ba trường riêng. Không dùng suggestion cho thiếu proof bảo mật, isolation, ngân sách hoặc recovery.</p></section>
<section aria-labelledby="boundaries"><h2 id="boundaries">Giữ phạm vi và quyền</h2><ul><li>Master-plan chuẩn về phạm vi/trạng thái; spec/ADR chuẩn về hợp đồng. Nguồn lệch nhau phải ghi nhận, không tự chọn trạng thái thuận lợi.</li><li>Test ghi DB, reset, kill/restart, migration hoặc restore cần tài nguyên kiểm định riêng và quyền đúng thao tác. Không có thì ghi blocked, tiếp tục phần độc lập.</li><li>Inference cần grant riêng theo phase, batch, mục đích, scope, model và hạn mức/expiry. Grant batch trước, nghiệm thu hoặc quyền phiên Codex không cấp lượt gọi mới.</li><li>Redact trước khi lưu. Không có secret thật, DB dump hay gateway transcripts trong evidence tracked. Unknown side effect không tự retry; replay chỉ đọc.</li><li>Kết luận: fail bắt buộc → cần sửa; còn blocked/not-run → chưa đủ bằng chứng; đủ pass/gate/evidence → đạt kỹ thuật. AI không tự nghiệm thu.</li></ul><p>Chi tiết điều kiện, C01–C08, severity và quy trình retest trong <a href="RULES.md">rule bắt buộc</a>.</p></section>
<section aria-labelledby="gates"><h2 id="gates">Các checkpoint phải có báo cáo riêng</h2><ul class="gates"><li>03 → IG03 · dữ liệu</li><li>08 → IG08 · quan sát</li><li>12 → IG12 · điều phối</li><li>16 → IG16 · tài chính</li><li>20 → IG20 · báo cáo</li><li>23 → R1–R8 + đủ IG</li></ul><p>Gate yêu cầu run thật không pass bằng mock. Thiếu capability/isolation/privacy dùng CG01: blocked + gap report, Chủ tịch quyết định phương án riêng.</p></section>
<section aria-labelledby="phases"><h2 id="phases">Tra cứu checklist theo phase</h2><p>Chọn một phase, đọc Markdown đầy đủ. Danh sách này không biểu thị trạng thái triển khai hoặc nghiệm thu.</p><div class="grid">{''.join(cards)}</div></section>
<section aria-labelledby="save"><h2 id="save">Tên file và liên kết từng vòng</h2><pre>docs/tests/results/phase-NN/&lt;timestamp&gt;-r001-test/
  report.md
  evidence/
    source-manifest.json
    commands.md
    … bằng chứng đã lọc
docs/remakes/phase-NN/&lt;timestamp&gt;-r001-remake/
  remake.md
  evidence/…
docs/tests/results/phase-NN/&lt;timestamp&gt;-r002-test/
  report.md
  evidence/…</pre><p>Timestamp: YYYYMMDDTHHMMSS+0700. Test r001 → remake r001 → retest r002. Report mới link Supersedes và Remake nguồn; sổ vòng ở results/phase-NN/README.md. Không ghi đè lịch sử hoặc đổi tên batch legacy.</p><pre>rtk proxy python3 docs/tests/scripts/render.py
rtk proxy python3 docs/tests/scripts/validate.py</pre><p class="muted">Hai lệnh chỉ xử lý bộ tài liệu local, không kết nối DB/gateway hoặc chạy test sản phẩm. Validator kiểm cấu trúc; AI vẫn phải đánh giá nội dung evidence.</p></section>
<footer><p>Markdown là nguồn chuẩn của bộ kiểm định. <a href="README.md">Hướng dẫn</a> · <a href="RULES.md">Rule đầy đủ</a> · <a href="templates/report.md">Mẫu báo cáo</a></p><small class="muted">Soạn từ nguồn local 08/10/2026. HTML được đồng bộ từ Markdown; không lưu trạng thái nghiệm thu trong trình duyệt.</small></footer>
</main></body></html>'''


if __name__ == '__main__':
    (BASE / 'index.html').write_text(render())
    print('Đã đồng bộ docs/tests/index.html từ Markdown; không test sản phẩm/inference.')
