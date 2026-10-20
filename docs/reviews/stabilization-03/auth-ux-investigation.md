# Owner authentication UX investigation — Stabilization Sprint 03

## Finding

The Owner secret forms in the 19/10 UI Lens capture are the expected anonymous/restricted state. The capture used a fresh browser context without an Owner session cookie; protected requests returned 401, so each protected panel rendered its local login form. This does not show repeated authentication inside one valid Owner session.

The distinction is visible in the evidence:

- [Anonymous UI Lens capture — Office desktop](../../../artifacts/ui-review/2026-10-19T03-07-33-519Z_c157a8d2-5c98-4bf5-846b-a202b1012c9a/office/desktop.png) and [Playground desktop](../../../artifacts/ui-review/2026-10-19T03-07-33-519Z_c157a8d2-5c98-4bf5-846b-a202b1012c9a/playground/desktop.png) show the secret form. The capture manifest records the affected restricted routes as 401.
- [Sprint 02 authenticated Office capture](../stabilization-02/evidence/authenticated-fresh/screenshots/office/1440x900.png) shows an authenticated session without a secret form.
- Sprint 03 used a new headless browser context, logged in with the existing local Owner credential, then visited Overview, Playground, Office, Work Orders, Inspector, Replay and Approvals. All seven route checks found no password field. Product logout succeeded. The credential value was neither logged nor included in evidence. See [browser result](evidence/browser-result.json) and [Office desktop](evidence/screenshots/office-before-1440x900.png) / [Office mobile](evidence/screenshots/office-before-390x844.png).

RuntimePanel and PlaygroundPanel check `/api/v1/owner/session` on mount and share the same-origin Owner cookie. Navigation preserves that cookie. Expiry/revocation returns the panel to its restricted state by design. Login creates a local Owner session and does not create an inference grant.

The shell badge `Cần session Owner` is a static route requirement label in `apps/web/src/App.tsx`; it does not reflect the authenticated state inside the panel. In the authenticated mobile screenshot it appears above a panel that shows `Chủ tịch đã xác thực` and `Đăng xuất`. This label can confuse reviewers, but it is not a repeated secret form or an authorization defect. It is recorded as a follow-up UX improvement; no authentication, CSRF, cookie or session controls were weakened.

## Capture inventory

Fourteen authenticated, redacted captures exist at 1440×900 and 390×844 across Office, Inspector and Replay before recovery, after snapshot recovery, offline, stale-heartbeat and heartbeat-recovered states. Historical Playground text, opaque event identifiers and the company-scope ID are blurred before each image is saved. The automated journey also recorded zero page errors and only Owner login/logout as POST requests; other observed application requests were reads.

The screenshots show the UI state and viewport, not a live run. The recovery overlay uses explicitly intercepted test fixtures; it is not Phase 08 acceptance evidence.

## Gemini review

No Gemini integration was available in this task environment, so no Gemini feedback is claimed.
