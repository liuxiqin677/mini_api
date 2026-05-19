from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import User
from app.schemas import FootprintResponse, ApiResponse
from app.services import FootprintService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/footprints/list", response_model=ApiResponse[List[FootprintResponse]])
async def get_footprint_list(
    target_type: Optional[str] = Query(None, description="目标类型: animal, plant"),
    action_type: Optional[str] = Query(None, description="操作类型: collect, edit, delete, feed, pet, water, fertilize"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    footprints = FootprintService.get_user_footprints(
        db, current_user.id, target_type, action_type, limit, offset
    )
    return ApiResponse(code=200, message="success", data=footprints)
