from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import (
    PetResponse, UserPetResponse, ApiResponse,
    CollectPetRequest, EditPetNameRequest, DeletePetRequest
)
from app.services.pet_service import PetService
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/user/collect/pet", response_model=ApiResponse)
async def collect_pet(
    request: CollectPetRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_pet = PetService.collect_pet(db, current_user.id, request.pet_id)
    if not user_pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    return ApiResponse(code=200, message="收集成功", data=True)


@router.get("/user/collect/pet/list", response_model=ApiResponse[List[UserPetResponse]])
async def get_user_pets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pets = PetService.get_user_pets(db, current_user.id)
    return ApiResponse(code=200, message="success", data=pets)


@router.post("/user/collect/pet/edit", response_model=ApiResponse)
async def edit_pet_name(
    request: EditPetNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_pet = PetService.edit_pet_name(db, request.pet_id, current_user.id, request.name)
    if not user_pet:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="编辑成功", data=True)


@router.delete("/user/collect/pet/delete", response_model=ApiResponse)
async def delete_pet(
    request: DeletePetRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = PetService.delete_pet(db, request.pet_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="删除成功", data=True)
