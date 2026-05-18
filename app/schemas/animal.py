from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.food import FoodResponse
from app.schemas.tool import ToolResponse


class AnimalResponse(BaseModel):
    id: int
    name: str
    emoji: str
    description: str
    rarity: str
    category: str
    is_collected: bool
    favorite_food_ids: Optional[List[int]] = None
    tool_ids: Optional[List[int]] = None
    world_ids: Optional[List[int]] = None
    foods: Optional[List[FoodResponse]] = None
    tools: Optional[List[ToolResponse]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class AnimalDetail(AnimalResponse):
    pass


class CollectAnimalRequest(BaseModel):
    animal_id: int = Field(..., description="动物ID")


class EditAnimalNameRequest(BaseModel):
    animal_id: int = Field(..., description="用户动物记录ID")
    name: str = Field(..., description="新名称")


class DeleteAnimalRequest(BaseModel):
    animal_id: int = Field(..., description="用户动物记录ID")
