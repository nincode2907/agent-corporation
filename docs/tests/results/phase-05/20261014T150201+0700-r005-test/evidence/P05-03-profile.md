# P05-03 / P05-04 / P05-07 — FIX VERIFIED ở persisted API

RUNTIME-VERIFIED trong FastAPI app/router thật +PostgreSQL disposable15591/head0007. Environmentfixturef8343154-21a2-4c9b-8f2b-24332b2b901a/company7a766a40-b43a-43a5-bec1-f92640112316. Secret/cookie/CSRF đều canary tạm không lưu. Script [tái lập](P05-profile-fixture.py).

Actual metadata: GET/v1/models7IDs; GET/api/models capabilities đã normalize: gpt-6.1-sol vàgpt-6-astra hỗ trợlow/medium/high/xhigh/max/ultra;gpt-6-luna tốiđamax, khôngultra. Catalog không entitlement.

| Thử | HTTP / postcondition |
| --- | --- |
| Agent giả header X-Actor/X-Owner, không session |401;0metadataGET|
| Owner login canary / profile view đầu |200;profileversion0;0metadataGET|
| Owner có cookie thiếu CSRF |403;0metadataGET|
| PUTgpt-6.1-sol/low |200/v1;2GETmetadata|
| PUTgpt-6.1-sol/max |200/v2;2GETmetadata|
| PUTgpt-6.1-sol/ultra+fallbackgpt-6-astra |200/v3;2GETmetadata|
| Unknownprimarynot-in-catalog-p05-r004 |422;GETprofilev3unchanged/audit3|
| Unsupportedminimal trênknownmodel |422;v3/audit3unchanged|
| Unknownfallback |422;v3/audit3unchanged|
| gpt-6-lunafallbackvớieffortultra |422;v3/audit3unchanged|
| Staleexpected_version0 |409;v3/audit3unchanged|
| Gatewayoffline15599(no listener),save |503;GETprofilev3/audit3unchanged|
| GETprofilekhigatewayoffline |200;0metadataGET|

Ba event OWNER_MODEL_PROFILE_UPDATED thực trong DB; version1→2→3. Mỗi successful save có chính xác hai GET/v1/models vàGET/api/models, khôngPOST. Invalid/offline không ghi row/version/event. API gate/Owner validation vẫn trước profile metadata; fake headers không đạt networkcatalog. Đây là FIX VERIFIED P05-03, không fallback/entitlement/inferencegrant.
