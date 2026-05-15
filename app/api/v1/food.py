from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import (
    FoodResponse, FoodDetail, UserFoodResponse, ApiResponse,
    CollectFoodRequest, EditFoodNameRequest, DeleteFoodRequest,
    UserFoodCollectionResponse
)
from app.services.food_service import FoodService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/foods/list", response_model=ApiResponse[List[FoodResponse]])
async def get_foods_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    foods = FoodService.get_all_foods(db, current_user.id)
    return ApiResponse(code=200, message="success", data=foods)


@router.get("/foods/detail", response_model=ApiResponse[FoodDetail])
async def get_food_detail(
    food_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    food = FoodService.get_food_by_id(db, food_id, current_user.id)
    if not food:
        raise HTTPException(status_code=404, detail="食物不存在")
    return ApiResponse(code=200, message="success", data=food)


@router.post("/user/collect/food", response_model=ApiResponse)
async def collect_food(
    request: CollectFoodRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_food = FoodService.collect_food(db, current_user.id, request.food_id)
    if not user_food:
        raise HTTPException(status_code=404, detail="食物不存在")
    return ApiResponse(code=200, message="收集成功", data=True)


@router.get("/user/collect/food/list", response_model=ApiResponse[List[UserFoodResponse]])
async def get_user_foods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    foods = FoodService.get_user_foods(db, current_user.id)
    return ApiResponse(code=200, message="success", data=foods)


@router.get("/user/collect/food/list-with-detail", response_model=ApiResponse[UserFoodCollectionResponse])
async def get_user_foods_with_detail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户收集的食物列表，包含食物详情和数量"""
    items, total_count = FoodService.get_user_foods_with_detail(db, current_user.id)
    return ApiResponse(code=200, message="success", data={
        "items": items,
        "total_count": total_count
    })


@router.post("/user/collect/food/edit", response_model=ApiResponse)
async def edit_food_name(
    request: EditFoodNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_food = FoodService.edit_food_name(db, request.food_id, current_user.id, request.name)
    if not user_food:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="编辑成功", data=True)


@router.delete("/user/collect/food/delete", response_model=ApiResponse)
async def delete_food(
    request: DeleteFoodRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = FoodService.delete_food(db, request.food_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="删除成功", data=True)
