from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import WorldResponse, WorldDetail, ApiResponse
from app.services.world_service import WorldService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/world/list", response_model=ApiResponse[List[WorldResponse]])
async def get_worlds_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    worlds = WorldService.get_all_worlds(db)
    return ApiResponse(code=200, message="success", data=worlds)


@router.get("/world/detail", response_model=ApiResponse[WorldDetail])
async def get_world_detail(
    world_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    world = WorldService.get_world_by_id(db, world_id)
    if not world:
        raise HTTPException(status_code=404, detail="世界不存在")
    return ApiResponse(code=200, message="success", data=world)
