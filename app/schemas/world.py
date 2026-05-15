from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.animal import AnimalResponse
from app.schemas.plant import PlantResponse
from app.schemas.tool import ToolResponse
from app.schemas.food import FoodResponse


class WorldResponse(BaseModel):
    id: int
    name: str
    emoji: str
    description: str
    bg_color: Optional[str] = None
    gradient: Optional[str] = None
    animal_ids: Optional[List[int]] = None
    plant_ids: Optional[List[int]] = None
    tool_ids: Optional[List[int]] = None
    food_ids: Optional[List[int]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class WorldDetail(WorldResponse):
    """世界详情，包含动物、植物、工具、食物的详细信息"""
    animals: Optional[List[AnimalResponse]] = None
    plants: Optional[List[PlantResponse]] = None
    tools: Optional[List[ToolResponse]] = None
    foods: Optional[List[FoodResponse]] = None
