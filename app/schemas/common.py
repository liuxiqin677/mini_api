from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')


class IdNameItem(BaseModel):
    """通用的 id + name + emoji 结构"""
    id: int
    name: str
    emoji: Optional[str] = None


class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="消息")
    data: Optional[T] = Field(default=None, description="数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None
            }
        }
