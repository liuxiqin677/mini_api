from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ToolResponse(BaseModel):
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


class ToolDetail(ToolResponse):
    pass


class UserToolWithDetail(BaseModel):
    """用户收集的工具，包含工具详情和数量"""
    id: int
    user_id: int
    tool_id: int
    name: str
    emoji: str
    description: Optional[str] = None
    rarity: str
    count: int
    # 工具详情
    tool_detail: ToolResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserToolCollectionResponse(BaseModel):
    """用户收集工具列表响应，包含列表和总数"""
    items: List[UserToolWithDetail]
    total_count: int


class CollectToolRequest(BaseModel):
    tool_id: int = Field(..., description="工具ID")


class UseToolRequest(BaseModel):
    tool_id: int = Field(..., description="工具ID")


class EditToolNameRequest(BaseModel):
    tool_id: int = Field(..., description="用户工具记录ID")
    name: str = Field(..., description="新名称")


class DeleteToolRequest(BaseModel):
    tool_id: int = Field(..., description="用户工具记录ID")
