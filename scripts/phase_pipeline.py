"""Read-only projection of saved AI test/remake history for the roadmap."""
from pathlib import Path
import os
import re
from urllib.parse import urlparse

CASE_ID = r"(?:C\d{2}|P\d{2}-\d{2}|[A-Z][A-Z0-9]*-\d+)"


def field(source, name):
    match = re.search(rf"^- {re.escape(name)}: (.+)$", source, re.M)
    return match[1].strip() if match else ""


def url(root, path):
    return os.path.relpath(path, root / "docs").replace(os.sep, "/")


def read_report(root, path):
    source = path.read_text()
    cases = []
    for match in re.finditer(rf"^### ({CASE_ID}) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)", source, re.M | re.S):
        body = match[3]
        evidence = re.findall(r"\[[^\]]+\]\(([^)]+)\)", field(body, "Evidence"))
        evidence_valid = bool(evidence) and all(
            urlparse(href).scheme in {"https", "http"} or (path.parent / href.split("#", 1)[0]).is_file()
            for href in evidence
        )
        cases.append({"id": match[1], "title": match[2], "tag": field(body, "Tag"),
                      "result": field(body, "Kết quả"), "actual": field(body, "Thực tế"),
                      "handling": field(body, "Xử lý/đề xuất"), "severity": field(body, "Mức độ"),
                      "rebuttal": field(body, "Kết quả phản biện"),
                      "mandatory": not field(body, "Bắt buộc").startswith("không"),
                      "evidence_valid": evidence_valid})
    checklist = root / f"docs/tests/phases/phase-{path.parent.parent.name[-2:]}.md"
    expected = {f"C{number:02d}" for number in range(1, 9)} | set(re.findall(r"^\| (P\d{2}-\d{2}) \|", checklist.read_text(), re.M)) if checklist.is_file() else set()
    ident = path.parent.parent.name[-2:]
    expected_gates = {"03": {"IG03"}, "08": {"IG08"}, "12": {"IG12"}, "16": {"IG16"}, "20": {"IG20"},
                      "23": {"IG03", "IG08", "IG12", "IG16", "IG20"} | {f"R{number}" for number in range(1, 9)}}.get(ident, set())
    gates = re.findall(r"^\| (IG\d{2}|R[1-8]) \| (PASS|FAIL|BLOCKED) \|", source, re.M)
    allowed = {"clean": {"pass"}, "suggestion": {"pass", "not-applicable"}, "need-change": {"fail", "blocked", "not-run"}}
    ready = bool(cases) and expected <= {case["id"] for case in cases} and all(
        case["result"] in allowed.get(case["tag"], set()) and case["evidence_valid"]
        and (case["id"] not in expected or (case["mandatory"] and case["result"] == "pass"))
        and (not case["mandatory"] or case["result"] == "pass")
        and case["rebuttal"] in {"", "none", "accepted", "rejected"}
        and not (case["rebuttal"] == "rejected" and case["result"] == "pass")
        and not (case["rebuttal"] == "accepted" and case["result"] != "pass")
        for case in cases
    ) and expected_gates <= {gate for gate, _ in gates} and all(verdict == "PASS" for _, verdict in gates)
    return {"kind": "test", "batch": path.parent.name, "round": field(source, "Vòng"),
            "actor": field(source, "Người/AI kiểm định"), "verdict": field(source, "Kết luận kỹ thuật"),
            "url": url(root, path), "cases": cases, "ready": ready}


def read_remake(root, path):
    source = path.read_text()
    actions = {}
    # Existing remakes use a mapping table, including rows grouping several IDs.
    for line in source.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5 or cells[3] not in {"changed", "blocked", "no-change", "rebutted"}:
            continue
        for ident in set(re.findall(CASE_ID, cells[0])):
            actions[ident] = {"id": ident, "status": cells[3], "reason": cells[1], "note": cells[2]}
    # Explicit per-finding fields are authoritative in new remakes.
    for match in re.finditer(rf"^### ({CASE_ID}) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)", source, re.M | re.S):
        status = field(match[3], "Trạng thái xử lý")
        if status in {"changed", "blocked", "no-change", "rebutted"}:
            actions[match[1]] = {"id": match[1], "status": status,
                                  "reason": field(match[3], "Nguyên nhân"),
                                  "note": field(match[3], "Phản biện") if status == "rebutted" else field(match[3], "Thay đổi")}
    return {"kind": "remake", "batch": path.parent.name, "round": field(source, "Vòng"),
            "actor": field(source, "Người/AI remake"), "verdict": field(source, "Kết luận vòng sửa"),
            "url": url(root, path), "actions": list(actions.values())}


def build_phase_pipeline(root: Path, ident: str):
    events = [read_report(root, path) for path in (root / "docs/tests/results" / f"phase-{ident}").glob("*/report.md")]
    events += [read_remake(root, path) for path in (root / "docs/remakes" / f"phase-{ident}").glob("*/remake.md")]
    def order(event):
        timestamp = re.match(r"\d{8}T\d{6}\+\d{4}", event["batch"])
        round_number = re.search(r"-r(\d+)-", event["batch"])
        # Round is the logical order. Parallel reviewers may prepare a batch
        # before the preceding remake's handoff document is saved.
        return (int(round_number[1]) if round_number else 0,
                (0 if event["kind"] == "test" else 1) if round_number else 0,
                timestamp[0] if timestamp else event["batch"], event["batch"])
    events.sort(key=order)
    issues = {}
    latest_report = None
    for event in events:
        if event["kind"] == "test":
            latest_report = event
            for case in event["cases"]:
                opened = case["tag"] == "need-change" or case["result"] in {"fail", "blocked", "not-run"}
                passed = case["result"] == "pass" and case["tag"] in {"clean", "suggestion"}
                if opened and case["id"] not in issues:
                    issues[case["id"]] = {"id": case["id"], "title": case["title"], "history": []}
                issue = issues.get(case["id"])
                if issue is None:
                    continue
                issue.update({"severity": case["severity"], "actual": case["actual"], "handling": case["handling"]})
                if opened:
                    issue.update({"state": "blocked" if case["result"] in {"blocked", "not-run"} else "open", "checked": False})
                elif passed and case["evidence_valid"]:
                    if issue.get("state") in {"rebuttal-pending", "rebuttal-rejected"} and case["rebuttal"] != "accepted":
                        issue.update({"state": "rebuttal-rejected" if case["rebuttal"] == "rejected" else "rebuttal-pending", "checked": False})
                    elif case["rebuttal"] == "rejected":
                        issue.update({"state": "open", "checked": False})
                    else:
                        issue.update({"state": "rebuttal-accepted" if case["rebuttal"] == "accepted" else "verified", "checked": True})
                elif passed:
                    issue.update({"state": "open", "checked": False})
                # Missing/invalid case outcomes never close an earlier issue.
                issue["history"].append({"kind": "test", "batch": event["batch"], "url": event["url"],
                                          "actor": event["actor"], "note": case["actual"],
                                          "outcome": case["result"], "rebuttal": case["rebuttal"]})
        else:
            for action in event["actions"]:
                issue = issues.get(action["id"])
                if issue is None:
                    continue
                # A remake records repair/rebuttal, but only a later test can close it.
                if issue.get("state") not in {"verified", "rebuttal-accepted"}:
                    state = {"changed": "fixed-pending", "rebutted": "rebuttal-pending",
                             "blocked": "blocked", "no-change": issue.get("state", "open")}[action["status"]]
                    issue.update({"state": state, "checked": state == "fixed-pending"})
                issue["history"].append({"kind": "remake", "batch": event["batch"], "url": event["url"],
                                          "actor": event["actor"], "note": action["note"],
                                          "outcome": action["status"], "reason": action["reason"]})
    unresolved = [issue for issue in issues.values() if issue.get("state") not in {"verified", "rebuttal-accepted"}]
    if not events:
        stage = "queued"
    elif events[-1]["kind"] == "remake" and any(issue["state"] in {"fixed-pending", "rebuttal-pending"} for issue in unresolved):
        stage = "retesting"
    elif unresolved:
        stage = "blocked" if all(issue["state"] == "blocked" for issue in unresolved) else "remaking"
    elif latest_report and latest_report["verdict"] == "đạt" and latest_report["ready"]:
        stage = "ok"
    else:
        stage = "testing"
    return {"stage": stage, "issues": list(issues.values()),
            "steps": [{key: event[key] for key in ("kind", "batch", "round", "actor", "verdict", "url")} for event in events],
            "open_count": len(unresolved)}
