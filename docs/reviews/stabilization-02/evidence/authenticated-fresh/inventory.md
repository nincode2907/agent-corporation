# Authenticated UI review inventory

Browser: Chromium 156.0.8078.4
Viewports: 1440×900 desktop; 390×844 mobile
Auth: Owner login succeeded; product logout succeeded.
Capture: read-only screen navigation. Session/profile/grant/message/approval/run writes were not performed.

## Screens

| Screen | Viewport | Heading | Page overflow | Screenshot |
| --- | --- | --- | --- | --- |
| overview | 1440×900 | Tổng quan | False | [screenshots/overview/1440x900.png](screenshots/overview/1440x900.png) |
| overview | 390×844 | Tổng quan | False | [screenshots/overview/390x844.png](screenshots/overview/390x844.png) |
| playground | 1440×900 | Playground | False | [screenshots/playground/1440x900.png](screenshots/playground/1440x900.png) |
| playground | 390×844 | Playground | False | [screenshots/playground/390x844.png](screenshots/playground/390x844.png) |
| office | 1440×900 | Văn phòng trực tiếp | False | [screenshots/office/1440x900.png](screenshots/office/1440x900.png) |
| office | 390×844 | Văn phòng trực tiếp | False | [screenshots/office/390x844.png](screenshots/office/390x844.png) |
| work | 1440×900 | Công việc | False | [screenshots/work/1440x900.png](screenshots/work/1440x900.png) |
| work | 390×844 | Công việc | False | [screenshots/work/390x844.png](screenshots/work/390x844.png) |
| inspector | 1440×900 | Agent Inspector | False | [screenshots/inspector/1440x900.png](screenshots/inspector/1440x900.png) |
| inspector | 390×844 | Agent Inspector | False | [screenshots/inspector/390x844.png](screenshots/inspector/390x844.png) |
| replay | 1440×900 | Phát lại | False | [screenshots/replay/1440x900.png](screenshots/replay/1440x900.png) |
| replay | 390×844 | Phát lại | False | [screenshots/replay/390x844.png](screenshots/replay/390x844.png) |
| organization | 1440×900 | Tổ chức | False | [screenshots/organization/1440x900.png](screenshots/organization/1440x900.png) |
| organization | 390×844 | Tổ chức | False | [screenshots/organization/390x844.png](screenshots/organization/390x844.png) |
| approvals | 1440×900 | Chờ Chủ tịch duyệt | False | [screenshots/approvals/1440x900.png](screenshots/approvals/1440x900.png) |
| approvals | 390×844 | Chờ Chủ tịch duyệt | False | [screenshots/approvals/390x844.png](screenshots/approvals/390x844.png) |
| settings | 1440×900 | Cấu hình & sức khỏe | False | [screenshots/settings/1440x900.png](screenshots/settings/1440x900.png) |
| settings | 390×844 | Cấu hình & sức khỏe | False | [screenshots/settings/390x844.png](screenshots/settings/390x844.png) |

## Read-only journeys

- **dashboard-office-inspector**: overview → office → inspector; authenticated navigation and read-only inspection.
- **dashboard-work-approval**: overview → work → approvals; authenticated navigation and read-only inspection.
- **playground-profile-grant-history**: playground; authenticated navigation and read-only inspection.
- **inspector-replay-source**: inspector → replay; authenticated navigation and read-only inspection.
- **organization-employee-list**: organization; authenticated navigation and read-only inspection.
- **replay-filter-seek-reload**: replay; runOptions=2, sliderPresent=True, reloadRecovered=True, eventReadRequests=2, businessWrites=[].

## Controlled state checks

- **cursor-gap-read-error**: observed=True; method=HTTP 409 read-only endpoint interception.
- **cursor-gap-reload-recovery**: observed=True; method=controlled route.
- **browser-offline**: observed=True; method=Chromium context.setOffline(true).
- **offline-recovery**: observed=True; method=Chromium context.setOffline(false).
- **stalled-heartbeat-stale**: observed=True; method=hold SSE request and advance browser Date.now by 31 seconds.
- **stalled-heartbeat-recovery**: observed=True; method=controlled route.

## Sanitization

Images visually blur historical Playground prompt/output text and opaque Inspector/Replay identifiers. The HTML does not embed DOM text or network bodies. The manifest contains only request method/path and booleans indicating cursor headers/parameters; it excludes cursor values, cookies, CSRF tokens, secret values and message bodies.
