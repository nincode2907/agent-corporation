# Sanitized UI/UX review package for lead mentor

## Journey question

Can the Owner tell which employee is executing, what task is active, whether the run is idle/waiting/executing/completed, where output/evidence lives, how to open Replay, and which token/cost values are unknown?

## Evidence available

- Runtime and Work Order screen copy/source is available in `apps/web/src/RuntimePanel.tsx`.
- Prior redacted Owner-authenticated Office, Inspector and Replay desktop/mobile states are indexed in [`Stabilization Sprint 03`](../../stabilization-03/evidence/commands.md). Those screenshots show read/recovery fixtures, not a live active Run.
- Sprint 04 changed the shell access label to `Yêu cầu quyền Owner`; the current shared runtime was not rebuilt, so that change is build-verified only.

## Questions for review

1. Does the Runtime form clearly distinguish a direct Run from a Work Order queue item and Playground turn?
2. How should Office explain that no employee is assigned to a Runtime Run today?
3. Are `waiting_model`, offline/stale and unknown usage/cost wording clear to an Owner?
4. Does the Inspector expose enough profile/version provenance without implying an employee assignment?
5. Does Replay make its read-only nature and history gaps clear?

Gemini was signed out in the available browser tab; no review request was sent and no Gemini response is claimed.
