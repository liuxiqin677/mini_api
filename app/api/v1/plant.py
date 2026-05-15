from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import (
    PlantResponse, PlantDetail, UserPlantResponse, ApiResponse,
    CollectPlantRequest, EditPlantNameRequest, DeletePlantRequest
)
from app.services.plant_service import PlantService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/plants/animals/list", response_model=ApiResponse[List[PlantResponse]])
async def get_plants_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plants = PlantService.get_all_plants(db, current_user.id)
    return ApiResponse(code=200, message="success", data=plants)


@router.get("/plants/detail", response_model=ApiResponse[PlantDetail])
async def get_plant_detail(
    plant_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plant = PlantService.get_plant_by_id(db, plant_id, current_user.id)
    if not plant:
        raise HTTPException(status_code=404, detail="植物不存在")
    return ApiResponse(code=200, message="success", data=plant)


@router.post("/user/collect/plant", response_model=ApiResponse)
async def collect_plant(
    request: CollectPlantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_plant = PlantService.collect_plant(db, current_user.id, request.plant_id)
    if not user_plant:
        raise HTTPException(status_code=404, detail="植物不存在")
    return ApiResponse(code=200, message="收集成功", data=True)


@router.get("/user/collect/plant/list", response_model=ApiResponse[List[UserPlantResponse]])
async def get_user_plants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plants = PlantService.get_user_plants(db, current_user.id)
    return ApiResponse(code=200, message="success", data=plants)


@router.post("/user/collect/plant/edit", response_model=ApiResponse)
async def edit_plant_name(
    request: EditPlantNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_plant = PlantService.edit_plant_name(db, request.plant_id, current_user.id, request.name)
    if not user_plant:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="编辑成功", data=True)


@router.delete("/user/collect/plant/delete", response_model=ApiResponse)
async def delete_plant(
    request: DeletePlantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = PlantService.delete_plant(db, request.plant_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="删除成功", data=True)
