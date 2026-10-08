from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from .factory import read_demo_dashboard, reset_demo_dataset

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
def reset(request: ResetRequest) -> dict[str, object]:
    if request.confirmed is not True:
        raise HTTPException(status_code=400, detail="Cần xác nhận trước khi đặt lại dữ liệu demo.")
    try:
        return reset_demo_dataset(get_session_factory())
    except SQLAlchemyError as error:
        raise HTTPException(status_code=409, detail="Không thể reset scope demo cố định; dữ liệu chưa được seed lại.") from error
