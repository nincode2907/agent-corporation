"""Check relative links and required Phase 13 case rows in report.md."""
import re
from pathlib import Path

report = Path(__file__).parent.parent / "report.md"
content = report.read_text(encoding="utf-8")
links = re.findall(r"\]\(([^)]+)\)", content)
missing = [
    value for value in links
    if not value.startswith(("#", "http://", "https://"))
    and not (report.parent / value.split("#", 1)[0]).exists()
]
ids = [f"C0{number}" for number in range(1, 9)] + [f"P13-0{number}" for number in range(1, 8)]
rows = [line for line in content.splitlines() if line.startswith("| ")]
missing_ids = [case_id for case_id in ids if not any(f"| {case_id} |" in row for row in rows)]
print(f"relative_links={len(links)} missing_links={missing} missing_ids={missing_ids}")
if missing or missing_ids:
    raise SystemExit(1)
