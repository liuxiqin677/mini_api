from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.food import FoodResponse
from app.schemas.tool import ToolResponse


class UserAnimalResponse(BaseModel):
    id: int
    user_id: int
    animal_id: int
    name: str
    original_name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    favorite_food_ids: Optional[List[int]] = None
    tool_ids: Optional[List[int]] = None
    foods: Optional[List[FoodResponse]] = None
    tools: Optional[List[ToolResponse]] = None
    love: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPlantResponse(BaseModel):
    id: int
    user_id: int
    plant_id: int
    name: str
    original_name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    favorite_food_ids: Optional[List[int]] = None
    tool_ids: Optional[List[int]] = None
    foods: Optional[List[FoodResponse]] = None
    tools: Optional[List[ToolResponse]] = None
    love: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FootprintResponse(BaseModel):
    id: int
    user_id: int
    action_type: str
    target_type: str
    target_id: int
    target_name: str
    detail: Optional[str] = None
    change_value: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# 培养请求类型
class NurtureType:
    FEED = "feed"          # 喂食
    PET = "pet"            # 抚摸
    WATER = "water"        # 浇水
    FERTILIZE = "fertilize" # 施肥


class NurtureRequest(BaseModel):
    target_type: str = Field(..., description="目标类型: animal 或 plant")
    target_id: int = Field(..., description="目标ID")
    action_type: str = Field(..., description="操作类型: feed, pet, water, fertilize")



class UserToolResponse(BaseModel):
    id: int
    user_id: int
    tool_id: int
    name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    count: int = 1
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserFoodResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    count: int = 1
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPetResponse(BaseModel):
    id: int
    user_id: int
    pet_id: int
    name: str
    description: Optional[str] = None
    rarity: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
