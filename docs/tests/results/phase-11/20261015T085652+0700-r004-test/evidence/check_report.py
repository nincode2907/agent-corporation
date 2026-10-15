"""Check that this report lists every required case and existing file link."""
from __future__ import annotations

import re
from pathlib import Path

report = Path(__file__).parent.parent / "report.md"
text = report.read_text(encoding="utf-8")
links = re.findall(r"\]\(([^)]+)\)", text)
missing = [
    link
    for link in links
    if not link.startswith("#") and not (report.parent / link.split("#", 1)[0]).exists()
]
ids = [f"C0{index}" for index in range(1, 9)] + [f"P11-0{index}" for index in range(1, 8)]
case_count = sum(text.count(f"### {case_id} —") for case_id in ids)
print(f"relative_links={len(links)} missing={missing} cases={case_count}")
if missing or case_count != len(ids):
    raise SystemExit(1)
