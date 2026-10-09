from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from .factory import read_demo_dashboard, reset_demo_dataset
from .factory import DEMO_SCOPE
from ..governance.auth import OwnerPrincipal, require_owner_write

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])


class ResetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirmed: bool


@router.get("/dashboard")
def dashboard() -> dict[str, object]:
    try:
        return read_demo_dashboard(get_session_factory())
    except SQLAlchemyError as error:
        raise HTTPException(status_code=503, detail="Không đọc được dữ liệu demo.") from error


@router.post("/reset")
def reset(request: ResetRequest, principal: OwnerPrincipal = Depends(require_owner_write)) -> dict[str, object]:
    if principal.scope != DEMO_SCOPE:
        raise HTTPException(status_code=403, detail="Chỉ reset scope demo đã được xác thực.")
    if request.confirmed is not True:
        raise HTTPException(status_code=400, detail="Cần xác nhận trước khi đặt lại dữ liệu demo.")
    try:
        return reset_demo_dataset(get_session_factory())
    except SQLAlchemyError as error:
        raise HTTPException(status_code=409, detail="Không thể reset scope demo cố định; dữ liệu chưa được seed lại.") from error
