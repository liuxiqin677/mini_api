from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.schemas import ApiResponse
from app.services.user_service import UserService
from app.core.security import create_access_token

router = APIRouter()


class LoginForm(BaseModel):
    username: str
    password: str


class LoginResult(BaseModel):
    token_type: str = "bearer"
    access_token: str


@router.post("/login", response_model=ApiResponse[LoginResult])
async def login_for_access_token(form_data: LoginForm, db: Session = Depends(get_db)):
    user = UserService.get_user_by_username(db, form_data.username)

    if not user:
        user = UserService.create_user(db, LoginForm(
            username=form_data.username,
            password=form_data.password
        ))
    else:
        if not UserService.authenticate_user(db, form_data.username, form_data.password):
            raise HTTPException(
                status_code=401,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token = create_access_token(data={"sub": user.username})

    return ApiResponse(
        code=200,
        message="success",
        data=LoginResult(
            token_type="bearer",
            access_token=access_token
        )
    )
