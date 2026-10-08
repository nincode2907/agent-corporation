#!/usr/bin/env python3
"""Dựng bản đặc tả/ADR trực quan từ Markdown rồi đồng bộ roadmap."""
from pathlib import Path
import html
import json
import re
import sys
sys.dont_write_bytecode = True
from render_plan import ROOT, prose, build as build_plan


def build():
    source = (ROOT / "docs/product-spec.md").read_text()
    blocks = list(re.finditer(r"^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\. |\Z)", source, re.M | re.S))
    if [int(b[1]) for b in blocks] != list(range(1, 18)):
        raise ValueError("Đặc tả cần đầy đủ 17 mục")
    sections = [{"id": "section-" + b[1].zfill(2), "title": b[2], "body": b[3]} for b in blocks]
    flow_section = next(s for s in sections if s["id"] == "section-04")
    steps = []
    for line in flow_section["body"].splitlines():
        if re.match(r"^\| [1-7] \|", line):
            c = [x.strip() for x in line.strip("|").split("|")]
            steps.append({"number": c[0], "actor": c[1], "action": c[2], "state": c[3], "evidence": c[4]})
    if len(steps) != 7:
        raise ValueError("F01 cần 7 bước")
    counts = {"requirements": len(re.findall(r"^\| REQ\d{2} \|", source, re.M)), "screens": len(re.findall(r"^\| S\d{2} \|", source, re.M)), "events": len(re.findall(r"^\| [A-Z_]+ \|.* \| \d{2}", sections[8]["body"], re.M))}
    toc = "".join(f'<a href="#{s["id"]}"><span>{i:02}</span>{html.escape(s["title"])}</a>' for i, s in enumerate(sections, 1))
    full = "".join(f'<details id="{s["id"]}"><summary><span>{i:02}</span>{html.escape(s["title"])}</summary><div class="doc-content">{prose(s["body"])}</div></details>' for i, s in enumerate(sections, 1))
    page = (ROOT / "docs/assets/spec-template.html").read_text()
    version = re.search(r"Phiên bản đặc tả: ([^ ·]+)", source).group(1)
    status = re.search(r"^> Trạng thái: ([^\n]+)", source, re.M).group(1)
    replacements = {"__SPEC_VERSION__": html.escape(version), "__SPEC_STATUS__": html.escape(status), "__TOC__": toc, "__SECTIONS__": full, "__FLOW_DATA__": json.dumps(steps, ensure_ascii=False).replace("<", "\\u003c"), "__REQ_COUNT__": str(counts["requirements"]), "__SCREEN_COUNT__": str(counts["screens"]), "__EVENT_COUNT__": str(counts["events"])}
    for marker, value in replacements.items():
        if marker not in page:
            raise ValueError(f"Template thiếu {marker}")
        page = page.replace(marker, value)
    (ROOT / "docs/product-spec.html").write_text(page)
    adr = (ROOT / "docs/decisions/0001-v1-foundation.md").read_text()
    adr_status = re.search(r"Trạng thái: ([^\n]+)", adr).group(1)
    styles = re.search(r"<style>(.*?)</style>", page, re.S).group(1)
    icon = re.search(r'<link rel="icon"[^>]+>', page).group(0)
    adr_page = '<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ADR-0001 · Baseline V1</title>' + icon + '<style>' + styles + '</style></head><body><header><div class="shell top"><a class="brand" href="../product-spec.html">Agent Corporation · Quyết định nền V1</a><a href="../master-plan.html#phase-00">Theo dõi Phase 00 ↗</a></div></header><main class="shell"><div class="notice">' + prose(adr_status + ' · Không cấp inference grant hoặc quyền bắt đầu Phase 01.') + '</div><article class="doc-content standalone">' + prose(adr) + '</article></main><footer class="shell">Nguồn chuẩn: <a href="0001-v1-foundation.md">ADR Markdown</a>. Bản trực quan đồng bộ cùng đặc tả.</footer></body></html>'
    (ROOT / "docs/decisions/0001-v1-foundation.html").write_text(adr_page)
    print(f"Đã dựng đặc tả + ADR HTML: {counts['requirements']} requirements, {counts['screens']} màn hình, {counts['events']} events; demo đặc tả không gọi runtime.")
    build_plan()


if __name__ == "__main__":
    build()
