from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FoodResponse(BaseModel):
    id: int
    name: str
    emoji: str
    description: str
    rarity: str
    is_collected: bool
    world_ids: Optional[List[int]] = None
    target_ids: Optional[List[int]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class FoodDetail(FoodResponse):
    pass


class UserFoodWithDetail(BaseModel):
    """用户收集的食物，包含食物详情和数量"""
    id: int
    user_id: int
    food_id: int
    name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    count: int
    # 食物详情
    food_detail: FoodResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserFoodCollectionResponse(BaseModel):
    """用户收集食物列表响应，包含列表和总数"""
    items: List[UserFoodWithDetail]
    total_count: int


class CollectFoodRequest(BaseModel):
    food_id: int = Field(..., description="食物ID")


class UseFoodRequest(BaseModel):
    food_id: int = Field(..., description="食物ID")


class EditFoodNameRequest(BaseModel):
    food_id: int = Field(..., description="用户食物记录ID")
    name: str = Field(..., description="新名称")


class DeleteFoodRequest(BaseModel):
    food_id: int = Field(..., description="用户食物记录ID")
