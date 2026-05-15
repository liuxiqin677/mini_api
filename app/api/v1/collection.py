from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import CollectionProgressResponse, ApiResponse
from app.services.collection_service import CollectionService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/collection/progress", response_model=ApiResponse[CollectionProgressResponse])
async def get_collection_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的图鉴收集进度"""
    progress = CollectionService.get_collection_progress(db, current_user.id)
    return ApiResponse(code=200, message="success", data=progress)
