"""Build a sanitized contact sheet and self-contained mentor-review ZIP."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = ROOT / "docs/reviews/stabilization-02/evidence"
SOURCE = EVIDENCE / "authenticated-fresh"
ARCHIVE = EVIDENCE / "authenticated-ui-review.zip"


def main() -> int:
    manifest_path = SOURCE / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    screenshots = manifest.get("screenshots", [])
    if len([item for item in screenshots if item["screen"] in {
        "overview", "playground", "office", "work", "inspector", "replay", "organization", "approvals", "settings"
    }]) != 18:
        raise SystemExit("Expected all 9 authenticated screens × 2 viewports before packaging.")
    cards = []
    for item in screenshots:
        rel = item["screenshot"]
        label = f"{item['screen']} · {item['viewport']['width']}×{item['viewport']['height']}"
        cards.append(f'<article><a href="{escape(rel)}"><img loading="lazy" src="{escape(rel)}" alt="{escape(label)}"></a><h2>{escape(label)}</h2><p>Heading: {escape(str(item.get("heading") or "(none)"))} · overflow: {str(item.get("horizontalOverflow"))}</p></article>')
    html = """<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agent Corporation — authenticated UI review</title>
<style>body{margin:0;background:#f2f4f0;color:#1e2922;font:15px/1.5 system-ui,sans-serif}header{padding:28px max(20px,calc((100vw - 1360px)/2));background:#fff;border-bottom:1px solid #d8ded7}h1{font-size:26px;margin:0}header p{max-width:900px;color:#526058}.grid{max-width:1360px;margin:24px auto;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:20px}article{background:#fff;border:1px solid #d8ded7;border-radius:10px;padding:12px;box-shadow:0 2px 8px #16251a0b}img{display:block;width:100%;height:420px;object-fit:contain;background:#eef1ec;border-radius:5px}h2{font-size:16px;margin:10px 2px 0}article p{margin:2px;color:#59665d;font-size:13px}footer{max-width:1360px;margin:20px auto;padding:0 20px 30px;color:#59665d;font-size:13px}</style>
<header><h1>Agent Corporation — authenticated UI review</h1><p>Captured from the local Owner-authenticated UI at 1440×900 and 390×844. The review session only navigated and read persisted demo/runtime state; it did not create grants, send messages, decide approvals, or submit runs. Historical Playground text and opaque identifiers are visually blurred in this external-review package.</p></header><main class="grid">""" + "".join(cards) + "</main><footer>Contact sheet links open the full sanitized PNG. See inventory.md and manifest.json for flows, state checks, dimensions and request-method/path metadata. No credentials, cookies, CSRF tokens, event cursor values or transcripts are included.</footer></html>"
    (SOURCE / "contact-sheet.html").write_text(html, encoding="utf-8")

    screen_items = [item for item in screenshots if item["screen"] in {
        "overview", "playground", "office", "work", "inspector", "replay", "organization", "approvals", "settings"
    }]
    rows = ["# Authenticated UI review inventory", "", f"Browser: Chromium {manifest['browserVersion']}",
            "Viewports: 1440×900 desktop; 390×844 mobile", "Auth: Owner login succeeded; product logout succeeded.",
            "Capture: read-only screen navigation. Session/profile/grant/message/approval/run writes were not performed.",
            "", "## Screens", "", "| Screen | Viewport | Heading | Page overflow | Screenshot |", "| --- | --- | --- | --- | --- |"]
    for item in screen_items:
        viewport = item["viewport"]
        rows.append(f"| {item['screen']} | {viewport['width']}×{viewport['height']} | {item.get('heading') or ''} | {item.get('horizontalOverflow')} | [{item['screenshot']}]({item['screenshot']}) |")
    rows.extend(["", "## Read-only journeys", ""])
    for flow in manifest.get("flows", []):
        description = flow.get("actions") or ", ".join(
            f"{key}={value}" for key, value in flow.items()
            if key not in {"id", "routes"}
        ) or "read-only navigation"
        rows.append(f"- **{flow['id']}**: {' → '.join(flow['routes'])}; {description}.")
    rows.extend(["", "## Controlled state checks", ""])
    for check in manifest.get("stateChecks", []):
        rows.append(f"- **{check['state']}**: observed={check.get('observed')}; method={check.get('method', check.get('injection', 'controlled route'))}.")
    rows.extend(["", "## Sanitization", "", "Images visually blur historical Playground prompt/output text and opaque Inspector/Replay identifiers. The HTML does not embed DOM text or network bodies. The manifest contains only request method/path and booleans indicating cursor headers/parameters; it excludes cursor values, cookies, CSRF tokens, secret values and message bodies."])
    (SOURCE / "inventory.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (SOURCE / "README.txt").write_text(
        "Authenticated Agent Corporation UI review package. Open contact-sheet.html in a browser.\n"
        "Screenshots are full-page PNGs; historical Playground text and opaque IDs are visually blurred.\n"
        "The Owner session was logged out after the read-only capture. No inference, grant, prompt, approval,\n"
        "profile change, or run was performed. manifest.json excludes secrets and request bodies.\n",
        encoding="utf-8",
    )
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file():
                package.write(path, Path("authenticated-ui-review") / path.relative_to(SOURCE))
    print(json.dumps({"zip": str(ARCHIVE), "screens": len(screen_items), "all_screenshots": len(screenshots), "contact_sheet": str(SOURCE / 'contact-sheet.html')}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
