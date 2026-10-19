"""Check report link targets and renderer-visible required cases."""
import re
from pathlib import Path

report = Path(__file__).parent.parent / "report.md"
content = report.read_text(encoding="utf-8")
links = re.findall(r"\]\(([^)]+)\)", content)
missing_links = [
    link for link in links
    if not link.startswith(("#", "http://", "https://"))
    and not (report.parent / link.split("#", 1)[0]).exists()
]
case_ids = [f"C0{i}" for i in range(1, 9)] + [f"P12-0{i}" for i in range(1, 8)]
headings = re.findall(r"^### ((?:C\d{2}|P\d{2}-\d{2}))(?: — [^\n]+)?$", content, re.M)
blocks = re.split(r"^### (?:C\d{2}|P\d{2}-\d{2})(?: — [^\n]+)?\n", content, flags=re.M)[1:]
missing_fields = []
for case_id, block in zip(headings, blocks):
    for field in ("Thực tế", "Tag", "Kết quả", "Mức độ", "Xử lý/đề xuất"):
        if not re.search(rf"^- {re.escape(field)}: .+", block, re.M):
            missing_fields.append(f"{case_id}:{field}")
missing_ids = [case_id for case_id in case_ids if case_id not in headings]
print(f"links={len(links)} missing_links={missing_links} cases={len(headings)} missing_ids={missing_ids} missing_fields={missing_fields}")
if missing_links or missing_ids or missing_fields:
    raise SystemExit(1)
