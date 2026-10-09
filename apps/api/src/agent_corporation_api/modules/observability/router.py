from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from ..governance.auth import OwnerPrincipal, cursor_signing_key, require_owner
from .feed import CursorError, EventGap, read_event_page

router = APIRouter(prefix="/api/v1/events", tags=["events"])
POLL_SECONDS = 1.0
HEARTBEAT_SECONDS = 10.0


def page(principal: OwnerPrincipal, cursor: str | None, limit: int = 100) -> dict:
    try:
        return read_event_page(get_session_factory(), scope=principal.scope,
                               session_id=str(principal.session_id), key=cursor_signing_key(), cursor=cursor, limit=limit)
    except EventGap as error:
        raise HTTPException(409, detail={"code": "event_gap", "message": str(error)}) from error
    except CursorError as error:
        raise HTTPException(400, detail={"code": "invalid_cursor", "message": str(error)}) from error
    except SQLAlchemyError as error:
        raise HTTPException(503, detail="Không đọc được event đã lưu.") from error


@router.get("")
def events(cursor: str | None = None, limit: int = Query(100, ge=1, le=200),
           principal: OwnerPrincipal = Depends(require_owner)) -> dict:
    return page(principal, cursor, limit)


def frame(event: str, data: dict, cursor: str | None = None) -> str:
    return (f"id: {cursor}\n" if cursor else "") + f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def event_frames(request: Request, principal: OwnerPrincipal, initial: dict):
    batch = initial
    elapsed = 0.0
    while not await request.is_disconnected():
        # A stream never inherits authorization indefinitely; expiry/logout are checked every poll.
        try:
            current = await asyncio.to_thread(require_owner, request)
            if current != principal:
                raise HTTPException(401, detail="Phiên/phạm vi đã đổi.")
        except HTTPException:
            yield frame("auth-expired", {"message": "Phiên Owner đã kết thúc; hãy đăng nhập lại."})
            return
        for item in batch["events"]:
            yield frame("domain", item, item["cursor"])
        if batch["events"] or elapsed >= HEARTBEAT_SECONDS:
            yield frame("heartbeat", {"cursor": batch["cursor"], "server_time": batch["server_time"],
                                      "meaning": "Kết nối event store; không phải heartbeat của agent."})
            elapsed = 0
        cursor = batch["cursor"]
        await asyncio.sleep(POLL_SECONDS)
        elapsed += POLL_SECONDS
        try:
            batch = await asyncio.to_thread(page, principal, cursor)
        except HTTPException as error:
            yield frame("gap" if error.status_code in (400, 409) else "unavailable",
                        {"message": error.detail, "requires_reload": True})
            return


@router.get("/stream")
def stream(request: Request, cursor: str | None = None,
           principal: OwnerPrincipal = Depends(require_owner)) -> StreamingResponse:
    header_cursor = request.headers.get("last-event-id")
    if header_cursor and cursor and header_cursor != cursor:
        raise HTTPException(400, detail="Cursor query và Last-Event-ID không khớp.")
    initial = page(principal, header_cursor or cursor)
    return StreamingResponse(event_frames(request, principal, initial), media_type="text/event-stream",
                             headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})
