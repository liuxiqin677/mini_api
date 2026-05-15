from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.schemas import (
    UserLogin, UserRegister, UserDetail, UserProgress, ApiResponse
)
from app.services.user_service import UserService
from app.api.deps import get_current_user
from app.core.security import create_access_token

router = APIRouter()


class LoginResult(BaseModel):
    token_type: str = "bearer"
    access_token: str


@router.post("/login", response_model=ApiResponse[LoginResult])
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.get_user_by_username(db, form_data.username)

    if not user:
        user = UserService.create_user(db, UserRegister(
            username=form_data.username,
            password=form_data.password
        ))
    else:
        if not UserService.authenticate_user(db, form_data.username, form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )

    access_token = create_access_token(data={"sub": user.username})
    return ApiResponse(
        code=200,
        message="success",
        data=LoginResult(token_type="bearer", access_token=access_token)
    )


@router.get("/detail", response_model=ApiResponse[UserDetail])
async def get_user_detail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_detail = UserService.get_user_detail(db, current_user.id)
    return ApiResponse(code=200, message="success", data=user_detail)


@router.get("/collect/progress", response_model=ApiResponse[UserProgress])
async def get_user_collect_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = UserService.get_user_progress(db, current_user.id)
    return ApiResponse(code=200, message="success", data=progress)
