#!/usr/bin/env python3
"""Validation hợp đồng/tài liệu Phase 00; không gọi HTTP, model, DB hoặc worker."""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
sys.dont_write_bytecode = True
from render_plan import ROOT


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rows(section, identifier):
    result = []
    for line in section.splitlines():
        if re.match(rf"^\| {identifier} \|", line):
            result.append([x.strip() for x in line.strip("|").split("|")])
    return result


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.lang = None
        self.icon = False
        self.inline_js = []
        self.json = {}
        self.script_type = None
        self.script_id = None
        self.script_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "icon":
            self.icon = attrs.get("href", "").startswith("data:image/svg+xml,")
        if tag == "script":
            self.script_type = attrs.get("type", "text/javascript")
            self.script_id = attrs.get("id")
            self.script_parts = []
            require("src" not in attrs, "Tài liệu không cần external scripts")

    def handle_data(self, text):
        if self.script_type is not None:
            self.script_parts.append(text)

    def handle_endtag(self, tag):
        if tag == "script":
            content = "".join(self.script_parts)
            if self.script_type == "application/json":
                self.json[self.script_id] = json.loads(content)
            else:
                self.inline_js.append(content)
            self.script_type = None
            self.script_parts = []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, help="File hashes phase blocks trước thay đổi, chỉ dùng kiểm tra phạm vi lần bàn giao")
    args = parser.parse_args()
    spec = (ROOT / "docs/product-spec.md").read_text()
    master = (ROOT / "docs/master-plan.md").read_text()
    sections = {int(m[1]): m[3] for m in re.finditer(r"^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\. |\Z)", spec, re.M | re.S)}
    require(sorted(sections) == list(range(1, 18)), "Đặc tả thiếu/trùng section")
    phases = {m[1]: m[0] for m in re.finditer(r"^### Phase (\d{2}) — [^\n]+\n(.*?)(?=^### Phase |^## 8\. |\Z)", master, re.M | re.S)}
    require(set(phases) == {f"{i:02}" for i in range(24)}, "Master plan thiếu phase")
    screens = rows(sections[3], r"S\d{2}")
    requirements = rows(sections[14], r"REQ\d{2}")
    require([r[0] for r in screens] == [f"S{i:02}" for i in range(1, 15)], "Screen IDs thiếu/trùng")
    require([r[0] for r in requirements] == [f"REQ{i:02}" for i in range(1, 27)], "Requirement IDs thiếu/trùng")
    for r in requirements:
        require(len(r) == 5 and all(r), f"Requirement thiếu field: {r[0]}")
        require(set(r[1].split("/")) <= {"I1", "I2", "P", "G"}, f"Source ref không rõ: {r[0]}")
        require(all(i in phases for i in re.findall(r"\b\d{2}\b", r[3])), f"Phase ref sai: {r[0]}")
        require(bool(re.findall(r"\b\d{2}\b", r[3])), f"Thiếu phase: {r[0]}")
    require(set(re.findall(r"\bS\d{2}\b", spec)) <= {r[0] for r in screens}, "Screen ref sai")
    require(set(re.findall(r"\bREQ\d{2}\b", spec)) == {r[0] for r in requirements}, "Requirement ref sai")
    require(len(rows(sections[4], r"[1-7]")) == 7 and len(rows(sections[4], r"F0[2-8]")) == 7, "Flow coverage cần F01–F08")
    require(len(rows(sections[13], r"R[1-8]")) == 8, "Release gates thiếu/trùng")
    decisions = rows(sections[15], r"D\d{2}")
    opens = rows(sections[15], r"O\d{2}")
    require([r[0] for r in decisions] == [f"D{i:02}" for i in range(1, 9)], "Decision IDs thiếu/trùng")
    require([r[0] for r in opens] == [f"O{i:02}" for i in range(1, 8)] and all(len(r) == 4 and all(r) for r in opens), "Open items cần owner/deadline")
    adr = (ROOT / "docs/decisions/0001-v1-foundation.md").read_text()
    require([r[0] for r in rows(adr, r"D\d{2}")] == [r[0] for r in decisions], "Spec và ADR lệch decisions")
    catalog = rows(sections[9], r"[A-Z_]+")
    event_types = {r[0] for r in catalog}
    # Phase06 adds four explicit Owner/run/grant audit types to the 31-type baseline.
    require(len(catalog) == len(event_types) == 35, "Event catalogue thiếu/trùng")
    require({"RUN_CREATED", "RUN_STOP_REQUESTED", "EXECUTION_GRANT_CREATED", "OWNER_MODEL_PROFILE_UPDATED"} <= event_types,
            "Thiếu event audit Owner/runtime Phase06")
    required_original = {"TASK_CREATED", "TASK_STARTED", "AGENT_ASSIGNED", "PLAN_UPDATED", "LLM_CALL_STARTED", "LLM_CALL_COMPLETED", "TOOL_CALL_STARTED", "TOOL_CALL_COMPLETED", "TOKEN_USAGE_RECORDED", "AGENT_HANDOFF", "APPROVAL_REQUESTED", "EVALUATION_COMPLETED", "TASK_COMPLETED", "TASK_FAILED"}
    require(required_original <= event_types, "Mất event types trong nguồn I2")
    task_states = {"draft", "queued", "planning", "awaiting_approval", "executing", "reviewing", "awaiting_acceptance", "rework", "paused", "blocked", "accepted", "failed", "cancelled"}
    transition_text = sections[8].split("### Run states")[0]
    transitions = rows(transition_text, r"[a-z_, ]+")
    require(bool(transitions), "Thiếu task transitions")
    for r in transitions:
        require(set(x.strip() for x in r[0].split(",")) <= task_states, "State nguồn sai")
        require(set(x.strip() for x in r[1].split(",")) <= task_states, "State đích sai")
        require(not ({"accepted", "failed", "cancelled"} & {x.strip() for x in r[0].split(",")}), "Terminal task có outgoing transition")
    for r in rows(sections[4], r"[1-7]"):
        require(set(re.findall(r"[a-z_]+", r[3])) <= task_states, "Demo dùng task state không khai báo")
    samples = [json.loads(m) for m in re.findall(r"```json\n(.*?)\n```", spec, re.S)]
    require(len(samples) == 2, "WorkOrder/Event JSON examples thiếu")
    work, event = samples
    require(work["status"] == "draft" and work["revision"] >= 1 and work["schema_version"] == 1, "WorkOrder state/version sai")
    require(work["execution_grant_id"] is None and work["budget_limits"]["max_model_requests"] == 0, "Sample không được cấp inference grant")
    require(bool(work["acceptance_criteria"]) and bool(work["expected_outputs"]), "Thiếu acceptance/output")
    require(event["schema_version"] == 1 and event["type"] in event_types and event["stream_seq"] > 0, "Event envelope sai")
    require(event["task_id"] == work["id"] and event["environment_id"] == work["environment_id"] and event["company_id"] == work["company_id"], "JSON example bị cross-scope")
    require(event["run_id"] is None and event["payload"]["fixture"] is True, "Sample chỉ là fixture, không run thật")
    for value in [work["id"], work["company_id"], work["environment_id"], event["event_id"], event["correlation_id"]]:
        uuid.UUID(value)
    print("PASS contract: 26 requirements/14 screens/8 flows/35 events/R1–R8; source/phase/decision/state refs và 2 JSON examples.")
    if args.baseline:
        before = json.loads(args.baseline.read_text())
        for ident, digest in before["phases"].items():
            if ident != "00":
                require(hashlib.sha256(phases[ident].encode()).hexdigest() == digest, f"Vượt phạm vi Phase {ident}")
        for name, digest in before["files"].items():
            if name.startswith("docs/sources/"):
                require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"Đã sửa nguồn gốc {name}")
        require(not any((ROOT / folder).exists() for folder in ["apps", "infra", "node_modules"]), "Đã scaffold ngoài Phase 00")
        print("PASS scope: blocks Phase 01–23 và nguồn ý tưởng giữ nguyên; không scaffold sản phẩm.")
    pages = [ROOT / "docs/master-plan.html", ROOT / "docs/product-spec.html", ROOT / "docs/decisions/0001-v1-foundation.html"]
    digests = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in pages}
    r = subprocess.run([sys.executable, str(ROOT / "scripts/render_phase00.py")], cwd=ROOT, capture_output=True, text=True)
    require(r.returncode == 0, r.stderr)
    for p in pages:
        require(hashlib.sha256(p.read_bytes()).hexdigest() == digests[p], f"HTML chưa đồng bộ với Markdown/template: {p.name}")
    node = shutil.which("node")
    require(node is not None, "Cần Node local để kiểm tra JavaScript syntax; không tự cài")
    with tempfile.TemporaryDirectory(prefix="agent-corporation-doc-check-") as tmp:
        for p in pages:
            content = p.read_text()
            require(not re.search(r"__[A-Z_]+__", content), f"Template marker còn sót: {p.name}")
            require(chr(8) not in content, f"Control character: {p.name}")
            page = Page()
            page.feed(content)
            require(page.lang == "vi" and page.icon, f"Thiếu lang=vi/favicon: {p.name}")
            require(len(page.ids) == len(set(page.ids)), f"Duplicate IDs: {p.name}")
            for href in page.links:
                if re.match(r"^https?://", href):
                    continue
                path, _, anchor = href.partition("#")
                target = (p.parent / path).resolve() if path else p
                require(target.is_file(), f"Local link không tồn tại: {href}")
                if anchor and target.suffix == ".html":
                    dest = Page()
                    dest.feed(target.read_text())
                    valid_virtual = target.name == "master-plan.html" and re.fullmatch(r"phase-\d{2}", anchor) and anchor[6:] in phases
                    require(anchor in dest.ids or bool(valid_virtual), f"Anchor không tồn tại: {href}")
            for i, js in enumerate(page.inline_js):
                require(not re.search(r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\b", js), f"Tài liệu có runtime/network client: {p.name}")
                out = Path(tmp) / f"{p.stem}-{i}.js"
                out.write_text(js)
                result = subprocess.run([node, "--check", str(out)], capture_output=True, text=True)
                require(result.returncode == 0, result.stderr)
            if p.name == "master-plan.html":
                plan = page.json["plan-data"]
                require(len(plan["phases"]) == 24, "Roadmap HTML thiếu phase")
                for q in plan["phases"]:
                    canonical_status = re.search(r"^- Trạng thái: (.+)$", phases[q["id"]], re.M)
                    require(canonical_status is not None and q["status"] == canonical_status[1], f"Trạng thái HTML lệch Markdown Phase {q['id']}")
                require(len(plan["phases"][0]["links"]) == 4, "Thiếu links artifact Phase 00")
            if p.name == "product-spec.html":
                require(len(page.json["flow-data"]) == 7, "HTML thiếu steps")
                require(page.json["flow-data"][0]["state"] == "draft" and page.json["flow-data"][-1]["state"] == "accepted", "HTML flow lệch source")
    print("PASS artifacts: 3 HTML đồng bộ/deterministic; links/anchors/IDs/lang=vi/favicon; JS syntax; không runtime/network client.")
    print("LIMIT: chưa chạy product tests/inference; chưa visual QA browser/mobile. Không suy Phase 00 đã được Chủ tịch nghiệm thu.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
