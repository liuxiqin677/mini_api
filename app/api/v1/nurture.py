from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import (
    NurtureRequest, UserAnimalResponse, UserPlantResponse, ApiResponse
)
from app.services import NurtureService
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/nurture/animal", response_model=ApiResponse[UserAnimalResponse])
async def nurture_animal(
    form_data: NurtureRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_animal = NurtureService.nurture_animal(
        db, current_user.id, form_data.target_id, form_data.action_type
    )
    if not user_animal:
        raise HTTPException(status_code=404, detail="动物不存在或操作类型不正确")
    return ApiResponse(code=200, message="success", data=user_animal)


@router.post("/nurture/plant", response_model=ApiResponse[UserPlantResponse])
async def nurture_plant(
    form_data: NurtureRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_plant = NurtureService.nurture_plant(
        db, current_user.id, form_data.target_id, form_data.action_type
    )
    if not user_plant:
        raise HTTPException(status_code=404, detail="植物不存在或操作类型不正确")
    return ApiResponse(code=200, message="success", data=user_plant)
