from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.food import FoodResponse
from app.schemas.tool import ToolResponse


class PlantResponse(BaseModel):
    id: int
    name: str
    emoji: str
    description: str
    rarity: str
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


class PlantDetail(PlantResponse):
    pass


class CollectPlantRequest(BaseModel):
    plant_id: int = Field(..., description="植物ID")


class EditPlantNameRequest(BaseModel):
    plant_id: int = Field(..., description="用户植物记录ID")
    name: str = Field(..., description="新名称")


class DeletePlantRequest(BaseModel):
    plant_id: int = Field(..., description="用户植物记录ID")
