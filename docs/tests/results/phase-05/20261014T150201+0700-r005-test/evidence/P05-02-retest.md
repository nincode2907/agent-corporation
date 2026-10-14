# P05-02 — FIX VERIFIED

Original reproduction: fake opener HTTP200bodyb"\xff" qua actual ASGI router. R004 trả500; source r005 trả **HTTP200,statuscontract_mismatch**. Không exception/secret/raw body trong response. Script thực thi [P05-profile-fixture.py](P05-profile-fixture.py) có assert đúng status vàactual output; 68test suite gồm3regression invalidUTF8, invalidJSON,nesting2000 cũng pass.

Happy actualGET15600 vẫn available/healthok/catalogok,7IDs,entitlementfalse. Offline/401/schema/429 và recovery ởbrowser ghi [UI](P05-ui-observation.md). Adapter chỉ catch parse ValueError/RecursionError tại json.loads; transport errors vẫnoffline, không che lỗi ngoài parse boundary. Không sửa/restart gateway.
