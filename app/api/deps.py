from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.security import decode_access_token
from app.services.user_service import UserService

security = HTTPBearer()


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="登录过期，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    user = UserService.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
