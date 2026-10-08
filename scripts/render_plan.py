#!/usr/bin/env python3
"""Đồng bộ HTML roadmap từ nguồn Markdown, chỉ dùng thư viện chuẩn."""
from pathlib import Path
import json
import re
import html

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/master-plan.md"
TEMPLATE = ROOT / "docs/assets/roadmap-template.html"
TARGET = ROOT / "docs/master-plan.html"
STATUSES = {"Chưa triển khai", "Đang triển khai", "Chờ nghiệm thu", "Hoàn tất", "Bị chặn"}


def inline(text):
    safe = html.escape(text)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    return re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', safe)


def prose(text):
    """Render khối tài liệu bổ trợ; trang chính dùng layout riêng."""
    out = []
    lines = text.strip().splitlines()
    n = 0
    while n < len(lines):
        line = lines[n]
        if not line.strip():
            n += 1
            continue
        if line.startswith("```"):
            n += 1
            block = []
            while n < len(lines) and not lines[n].startswith("```"):
                block.append(lines[n])
                n += 1
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
        elif line.startswith("|"):
            rows = []
            while n < len(lines) and lines[n].startswith("|"):
                cells = [c.strip() for c in lines[n].strip("|").split("|")]
                if not all(re.fullmatch(r"[: -]+", c) for c in cells):
                    rows.append(cells)
                n += 1
            out.append('<div class="table-wrap"><table>')
            for i, cells in enumerate(rows):
                tag = "th" if i == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            out.append("</table></div>")
            continue
        elif line.startswith("- ") or re.match(r"^\d+\. ", line):
            out.append("<ul>")
            while n < len(lines) and (lines[n].startswith("- ") or re.match(r"^\d+\. ", lines[n])):
                out.append("<li>" + inline(re.sub(r"^(?:- |\d+\. )", "", lines[n])) + "</li>")
                n += 1
            out.append("</ul>")
            continue
        elif line.startswith("#"):
            level = min(len(line) - len(line.lstrip("#")), 4)
            out.append(f"<h{level}>" + inline(line.lstrip("# ")) + f"</h{level}>")
        else:
            out.append("<p>" + inline(line.lstrip("> ")) + "</p>")
        n += 1
    return "".join(out)


def section(source, number):
    match = re.search(rf"^## {number}\. [^\n]+\n(.*?)(?=^## \d+\. |\Z)", source, re.M | re.S)
    if not match:
        raise ValueError(f"Thiếu mục {number}")
    return match.group(1).strip()


def build():
    source = SOURCE.read_text()
    version_match = re.search(r"Phiên bản kế hoạch: ([^ ·]+)", source)
    date_match = re.search(r"Ngày lập: (\d{2}/\d{2}/\d{4})", source)
    if not version_match or not date_match:
        raise ValueError("Thiếu phiên bản/ngày lập kế hoạch")
    version = version_match.group(1)
    date = date_match.group(1)
    phases = []
    for match in re.finditer(r"^### Phase (\d{2}) — ([^\n]+)\n(.*?)(?=^### Phase |^## 8\. |\Z)", source, re.M | re.S):
        ident, title, body = match.groups()
        meta = dict(re.findall(r"^- (Mốc|Trạng thái|Phụ thuộc|Mục tiêu): (.+)$", body, re.M))
        if set(meta) != {"Mốc", "Trạng thái", "Phụ thuộc", "Mục tiêu"} or meta["Trạng thái"] not in STATUSES:
            raise ValueError(f"Metadata không hợp lệ Phase {ident}")
        fields = {}
        for heading, content in re.findall(r"^#### ([^\n]+)\n(.*?)(?=^#### |\Z)", body, re.M | re.S):
            fields[heading] = content.strip()
        required = {"Phạm vi", "Có gì mới", "Demo", "Nghiệm thu", "Bàn giao", "Giới hạn", "Bằng chứng cần có", "Nhật ký triển khai"}
        if not required.issubset(fields):
            raise ValueError(f"Thiếu field Phase {ident}: {required - set(fields)}")
        links = [{"label": label, "href": href} for label, href in re.findall(r"^- \[([^]]+)\]\(([^)]+)\)$", fields.get("Tài liệu liên quan", ""), re.M)]
        for link in links:
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link["href"]) or not (SOURCE.parent / link["href"].split("#")[0]).is_file():
                raise ValueError(f"Tài liệu Phase {ident} không hợp lệ: {link['href']}")
        phases.append({"id": ident, "title": title, "milestone": meta["Mốc"], "status": meta["Trạng thái"], "deps": meta["Phụ thuộc"], "goal": meta["Mục tiêu"], "scope": fields["Phạm vi"].splitlines(), "new": fields["Có gì mới"].splitlines(), "checks": fields["Nghiệm thu"].splitlines(), "demo": fields["Demo"], "delivery": fields["Bàn giao"], "limit": fields["Giới hạn"], "evidence": fields["Bằng chứng cần có"], "history": fields["Nhật ký triển khai"], "links": links})
    if [p["id"] for p in phases] != [f"{i:02}" for i in range(24)]:
        raise ValueError("Kế hoạch cần phase 00–23, duy nhất và đúng thứ tự")
    raw_milestones = re.findall(r"^\| ([A-E]) \| ([^|]+) \| ([^|]+) \|$", section(source, 2), re.M)
    milestones = [{"id": i, "range": r.strip(), "value": value.strip()} for i, r, value in raw_milestones]
    if len(milestones) != 5:
        raise ValueError("Thiếu mốc A–E")
    payload = json.dumps({"version": version, "phases": phases, "milestones": milestones}, ensure_ascii=False).replace("<", "\\u003c")
    page = TEMPLATE.read_text()
    replacements = {"__PLAN_VERSION__": html.escape(version), "__PLAN_DATE__": html.escape(date.replace("/", ".")), "__PLAN_DATA__": payload, "__RULES__": prose(section(source, 3)), "__ARCHITECTURE__": prose(section(source, 4)), "__AUDIT__": prose(section(source, 5)), "__GUIDE__": prose(section(source, 6)), "__RELEASE__": prose(section(source, 8)), "__AFTER__": prose(section(source, 9)), "__SOURCES__": prose(section(source, 10))}
    for marker, content in replacements.items():
        if marker not in page:
            raise ValueError(f"Template thiếu {marker}")
        page = page.replace(marker, content)
    TARGET.write_text(page)
    print(f"Đã đồng bộ {TARGET.relative_to(ROOT)}: {len(phases)} phase; {sum(p['status'] == 'Hoàn tất' for p in phases)} hoàn tất.")


if __name__ == "__main__":
    build()
