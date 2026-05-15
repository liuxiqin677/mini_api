from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserAnimalResponse(BaseModel):
    id: int
    user_id: int
    animal_id: int
    name: str
    description: Optional[str] = None
    rarity: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPlantResponse(BaseModel):
    id: int
    user_id: int
    plant_id: int
    name: str
    description: Optional[str] = None
    rarity: str
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
