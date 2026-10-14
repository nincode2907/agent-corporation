# Source/UI observations

- S06 route in `App.tsx` precedes demo/other branches; Office/Inspector/replay and WorkBoard branches remain. Source inspection only; no browser/mobile/keyboard capture.
- Observatory EventSource retains fixed initial cursor; onerror only changes connection state. Mismatched Last-Event-ID probe returns HTTP 400.
- Work queue remains board/action oriented; no worker lease/recovery or retry/attempt lineage observed.
- Phase10 approvals UI source exists; empty/history/decision states not exercised.
