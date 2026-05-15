from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PetResponse(BaseModel):
    id: int
    name: str
    emoji: str
    description: str
    rarity: str
    is_collected: bool
    world_ids: Optional[List[int]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class CollectPetRequest(BaseModel):
    pet_id: int = Field(..., description="宠物ID")


class EditPetNameRequest(BaseModel):
    pet_id: int = Field(..., description="用户宠物记录ID")
    name: str = Field(..., description="新名称")


class DeletePetRequest(BaseModel):
    pet_id: int = Field(..., description="用户宠物记录ID")
