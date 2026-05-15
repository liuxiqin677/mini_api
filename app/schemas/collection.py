from pydantic import BaseModel
from typing import List, Optional


class CollectionProgressItem(BaseModel):
    """图鉴进度项"""
    id: str
    name: str
    emoji: str
    collected_count: int
    total_count: int
    progress: int
    bg_color: Optional[str] = None
    description: Optional[str] = None


class CollectionProgressResponse(BaseModel):
    """图鉴进度响应"""
    items: List[CollectionProgressItem]
