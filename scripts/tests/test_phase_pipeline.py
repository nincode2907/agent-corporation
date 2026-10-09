"""Regression checks for issue lifecycle; only temporary Markdown fixtures."""
from pathlib import Path
import sys
import json
import re
import subprocess
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from phase_pipeline import build_phase_pipeline


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def report(self, number, outcomes, verdict="cần sửa"):
        path = self.root / f"docs/tests/results/phase-05/20261009T10{number:04d}+0700-r{number:03d}-test/report.md"
        path.parent.mkdir(parents=True)
        (path.parent / 'evidence.md').write_text('Observed evidence')
        body = f"- Vòng: r{number:03d}\n- Người/AI kiểm định: tester\n- Kết luận kỹ thuật: {verdict}\n"
        for ident, tag, result, rebuttal in outcomes:
            body += f"\n### {ident} — Issue {ident}\n\n- Tag: {tag}\n- Kết quả: {result}\n- Thực tế: observed {result}\n- Kết quả phản biện: {rebuttal}\n- Evidence: [evidence](evidence.md)\n"
        path.write_text(body)

    def remake(self, number, status="changed", ids="P05-02"):
        path = self.root / f"docs/remakes/phase-05/20261009T10{number:04d}+0700-r{number:03d}-remake/remake.md"
        path.parent.mkdir(parents=True)
        path.write_text(f"- Người/AI remake: builder\n| {ids} | reason | actual change | {status} | retest |\n")

    def pipeline(self):
        return build_phase_pipeline(self.root, "05")

    def test_fixed_tick_is_pending_until_independent_retest(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(2)
        pipeline = self.pipeline()
        self.assertEqual(pipeline["stage"], "retesting")
        self.assertTrue(pipeline["issues"][0]["checked"])
        self.assertEqual(pipeline["open_count"], 1)
        self.report(3, [("P05-02", "clean", "pass", "none")], "đạt")
        pipeline = self.pipeline()
        self.assertEqual(pipeline["stage"], "ok")
        self.assertEqual(pipeline["issues"][0]["state"], "verified")
        self.assertEqual(len(pipeline["issues"][0]["history"]), 3)

    def test_failed_retest_reopens_and_removes_tick(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(2)
        self.report(3, [("P05-02", "need-change", "fail", "none")])
        self.assertEqual(self.pipeline()["issues"][0]["state"], "open")
        self.assertFalse(self.pipeline()["issues"][0]["checked"])

    def test_rebuttal_does_not_close_itself(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(2, "rebutted")
        self.assertEqual(self.pipeline()["issues"][0]["state"], "rebuttal-pending")
        self.assertFalse(self.pipeline()["issues"][0]["checked"])
        self.report(3, [("P05-02", "clean", "pass", "accepted")], "đạt")
        self.assertEqual(self.pipeline()["issues"][0]["state"], "rebuttal-accepted")
        self.assertEqual(self.pipeline()["stage"], "ok")

    def test_rejected_or_blocked_rebuttal_remains_open(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(2, "rebutted")
        self.report(3, [("P05-02", "need-change", "blocked", "rejected")], "chưa đủ bằng chứng")
        self.assertEqual(self.pipeline()["stage"], "blocked")
        self.assertFalse(self.pipeline()["issues"][0]["checked"])

    def test_rejected_rebuttal_with_inconsistent_pass_never_becomes_ok(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(2, "rebutted")
        self.report(3, [("P05-02", "clean", "pass", "rejected")], "đạt")
        self.assertFalse(self.pipeline()["issues"][0]["checked"])
        self.assertEqual(self.pipeline()["issues"][0]["state"], "rebuttal-rejected")
        self.assertNotEqual(self.pipeline()["stage"], "ok")

    def test_same_second_orders_test_before_its_remake(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(1)
        pipeline = self.pipeline()
        self.assertEqual(pipeline["stage"], "retesting")
        self.assertEqual(len(pipeline["issues"][0]["history"]), 2)
        self.assertTrue(pipeline["issues"][0]["checked"])

    def test_parallel_batch_start_does_not_reopen_pending_fix_after_retest(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.remake(1)
        document = next((self.root / "docs/remakes").glob("*/*/remake.md"))
        document.parent.rename(document.parent.parent / "20261009T200000+0700-r001-remake")
        self.report(2, [("P05-02", "need-change", "blocked", "none")], "chưa đủ bằng chứng")
        pipeline = self.pipeline()
        self.assertEqual(pipeline["stage"], "blocked")
        self.assertFalse(pipeline["issues"][0]["checked"])
        self.assertEqual([step["kind"] for step in pipeline["issues"][0]["history"]],
                         ["test", "remake", "test"])

    def test_verdict_without_evidence_or_with_failed_gate_is_not_ok(self):
        self.report(1, [("P05-02", "clean", "pass", "none")], "đạt")
        path = next((self.root / "docs/tests/results").glob("*/*/report.md"))
        path.write_text(path.read_text() + '\n| IG03 | BLOCKED | P05-02 | evidence |\n')
        self.assertNotEqual(self.pipeline()["stage"], "ok")
        path.write_text(path.read_text().split('\n| IG03')[0])
        path.parent.joinpath('evidence.md').unlink()
        self.assertNotEqual(self.pipeline()["stage"], "ok")

    def test_missing_case_in_latest_report_never_closes_old_issue(self):
        self.report(1, [("P05-02", "need-change", "fail", "none")])
        self.report(2, [("C01", "clean", "pass", "none")], "đạt")
        self.assertEqual(self.pipeline()["open_count"], 1)
        self.assertNotEqual(self.pipeline()["stage"], "ok")

    def test_required_checklist_cases_cannot_be_marked_optional_to_get_ok(self):
        checklist = self.root / 'docs/tests/phases/phase-05.md'
        checklist.parent.mkdir(parents=True)
        checklist.write_text('| P05-01 | Required case |\n')
        outcomes = [(f'C{number:02d}', 'clean', 'pass', 'none') for number in range(1, 9)]
        outcomes.append(('P05-01', 'clean', 'pass', 'none'))
        self.report(1, outcomes, 'đạt')
        self.assertEqual(self.pipeline()['stage'], 'ok')
        path = next((self.root / 'docs/tests/results').glob('*/*/report.md'))
        source = path.read_text()
        path.write_text(source.replace('### P05-01 — Issue P05-01', '### P05-01 — Issue P05-01\n- Bắt buộc: không'))
        self.assertNotEqual(self.pipeline()['stage'], 'ok')
        path.write_text(source.replace('### C01 — Issue C01\n\n- Tag: clean\n- Kết quả: pass', '### C01 — Issue C01\n- Bắt buộc: không\n- Tag: suggestion\n- Kết quả: not-applicable'))
        self.assertNotEqual(self.pipeline()['stage'], 'ok')

    def test_grouped_legacy_mapping_and_explicit_override(self):
        self.report(1, [("C03", "need-change", "fail", "none"), ("C06", "need-change", "fail", "none")])
        self.remake(2, ids="C03, C06")
        self.assertTrue(all(issue["checked"] for issue in self.pipeline()["issues"]))
        path = next((self.root / "docs/remakes").glob("*/*/remake.md"))
        path.write_text(path.read_text() + "\n### C06 — Finding\n- Trạng thái xử lý: rebutted\n- Phản biện: Contract evidence\n")
        by_id = {issue["id"]: issue for issue in self.pipeline()["issues"]}
        self.assertEqual(by_id["C06"]["state"], "rebuttal-pending")
        self.assertEqual(by_id["C03"]["state"], "fixed-pending")

    def test_no_reports_is_queued_and_suggestions_do_not_create_issues(self):
        self.assertEqual(self.pipeline()["stage"], "queued")
        self.report(1, [("P05-02", "suggestion", "pass", "none")], "đạt")
        self.assertEqual(self.pipeline()["stage"], "ok")
        self.assertEqual(self.pipeline()["issues"], [])

    def test_ui_renders_ai_ticks_and_history_without_manual_checkbox(self):
        template = Path(__file__).resolve().parents[2] / 'docs/assets/roadmap-template.html'
        source = template.read_text()
        functions = source[source.index('const issueLabels='):source.index('function updateCheckProgress()')]
        data = {'status': 'Chờ nghiệm thu', 'test_report': {'url': 'report.md', 'cases': []},
                'test_pipeline': {'stage': 'remaking', 'open_count': 2, 'steps': [], 'issues': [
                    {'id': 'P05-02', 'title': 'Fixed', 'state': 'fixed-pending', 'checked': True, 'actual': 'fixed',
                     'history': [{'kind': 'remake', 'outcome': 'changed', 'note': 'change', 'url': 'remake.md'}]},
                    {'id': 'C03', 'title': 'Rebutted', 'state': 'rebuttal-rejected', 'checked': False, 'actual': 'issue',
                     'history': [{'kind': 'test', 'outcome': 'fail', 'note': 'proof', 'url': 'report.md'}]}
                ]}}
        script = f"const data={json.dumps(data)}; const node={{innerHTML:''}}; const selected='05'; const phase=()=>data; const $=()=>node; const esc=x=>String(x??'');\n"
        script += functions + "\nrenderTests(); const assert=require('node:assert/strict'); assert(!node.innerHTML.includes('<input')); assert(!node.innerHTML.includes('data-followup')); assert(node.innerHTML.includes('Đã review có lỗi, chờ remake')); assert(node.innerHTML.includes('Đã remake, chờ review')); assert(node.innerHTML.includes('Review bác phản biện, chờ remake')); assert(node.innerHTML.includes('remake.md')); assert(node.innerHTML.includes('✓'));"
        subprocess.run(['/Users/buivannin/.local/bin/rtk', 'proxy', 'node'], input=script, text=True, check=True, capture_output=True)

    def test_document_inline_javascript_syntax(self):
        template = Path(__file__).resolve().parents[2] / 'docs/assets/roadmap-template.html'
        script = re.findall(r'<script[^>]*>(.*?)</script>', template.read_text(), re.S)[-1]
        subprocess.run(['/Users/buivannin/.local/bin/rtk', 'proxy', 'node', '--check'], input=script, text=True, check=True, capture_output=True)


if __name__ == "__main__":
    unittest.main()
