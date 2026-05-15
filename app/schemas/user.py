from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserRegister(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    id: int
    username: str
    token: str
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    id: int
    username: str
    level: int
    food_count: int
    tool_count: int
    pet_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    user_id: int
    collected_count: int
    total_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
