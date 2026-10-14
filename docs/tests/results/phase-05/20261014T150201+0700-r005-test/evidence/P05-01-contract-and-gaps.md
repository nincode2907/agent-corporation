# Current contract và P05-06 blocker

Đọc lại gatewaysource README/server/schema/provider/config/catalog và app adapter/profile; hashes [manifest](source-manifest.json). Actual probeGET15600 hiện available,health/catalogok,7modelIDs,auth_configuredfalse,entitlementfalse. Explicit profile save chỉGET/v1/models +GET/api/models; profile read/startup không probe. Gateway api/models cócapabilities theo model; adapter intersect liveIDs +chat_supported +efforts, không đưa price/privatefields vào profile.

Probe cũ vẫn đúng2GET/health +/v1/models; no stream/max_tokens. Runtime429queue/unknown/fallback đã rerun68tests trongfixturePG vàfake transport. Owner/model/tools/policy snapshot và nofallbackngoàiallowlist vẫnđúng; không gọiworker/gatewayPOST.

CG01 rerun thực hiện bằng check_gate(.local/cg01-proof.json,../codex-server,base_url15600):

```json
{"allowed":false,"reason":"missing_or_invalid_proof","fingerprint":"78f0a5ae3caa013fe3f667aee69855f08711380e6da3c98e51d56cce10b80a37"}
```

Gateway source fingerprint không đổi; tools disabled và ignore rules/config là hardeningsource, không thay evidence thực vềisolation/inputboundary,privacy-retention,cancellation. Chat route vẫn không ephemeral; không đọc native transcripts hoặc kết luận đãexploit file read. Cần trusted operator proof đúng fingerprint/endpoint/expiry/evidence hoặcquyếtđịnh contingency theo spec§6. Grant thật0; nếu đợt tiếp cần inference phải grant mới riêng, khôngkếthừa. Không sửa sharedgateway hoặc tạo instance khác.
