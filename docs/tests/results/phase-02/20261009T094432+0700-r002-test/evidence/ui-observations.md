# UI observations — Phase 02 r002

- Local page: `http://agent-corporation.localhost/#overview`; project fixture shows “Demo Corporation · fixture”, “Inference grant — Chưa được cấp”, demo metrics explicitly label “DOANH NGHIỆP GIẢ LẬP DEMO”, “5 Work Order · 20 event fixture”, usage “Chưa xác định”, and explanatory text “chi phí không phải 0”.
- Navigation visited in the browser: S01 Tổng quan → S05 Công việc (5 demo Work Orders) → S03 Agent Inspector shell; S06 Chờ Chủ tịch duyệt (one fixture) → S09 Tài chính (usage unknown) → S07 Tổ chức (DEMO fixture). Reload kept the selected route.
- Owner mode keyboard: Tab focused the Vận hành checkbox; Space changed view to Vận hành; mouse restored Chủ tịch. UI text explicitly states mode changes presentation only and does not change API permission.
- On one organization reload, the DOM briefly showed “Không đọc được demo. Seed tường minh…”; on the subsequent AX read the error was gone and demo organization data appeared. This was incidental natural loading, not a controlled network outage or a validated retry action.
- Desktop screenshot was visually inspected in the CUA response at the browser’s default wide viewport. It is not retained as an evidence file. No 390×844 viewport override or screenshot-to-workspace API was available in the enabled UI surface, so P02-06 lacks the required measured viewport and saved image.
- No page action seeded/reset data, invoked tools, or called a model.
