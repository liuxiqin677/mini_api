from pydantic import BaseModel
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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
