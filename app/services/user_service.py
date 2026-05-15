from typing import Optional
from sqlalchemy.orm import Session
from app.models import (
    User, UserAnimal, UserPlant, UserTool, UserFood, UserPet,
    Animal, Plant, Tool, Food, Pet
)
from app.schemas import UserRegister, UserDetail, UserProgress
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserRegister) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            hashed_password=hashed_password,
            level=1
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_detail(db: Session, user_id: int) -> Optional[UserDetail]:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None

        food_count = db.query(UserFood).filter(UserFood.user_id == user_id).count()
        tool_count = db.query(UserTool).filter(UserTool.user_id == user_id).count()
        pet_count = db.query(UserPet).filter(UserPet.user_id == user_id).count()

        return UserDetail(
            id=user.id,
            username=user.username,
            level=user.level,
            food_count=food_count,
            tool_count=tool_count,
            pet_count=pet_count,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    def get_user_progress(db: Session, user_id: int) -> UserProgress:
        user_animals = db.query(UserAnimal).filter(UserAnimal.user_id == user_id).count()
        user_plants = db.query(UserPlant).filter(UserPlant.user_id == user_id).count()
        user_tools = db.query(UserTool).filter(UserTool.user_id == user_id).count()
        user_foods = db.query(UserFood).filter(UserFood.user_id == user_id).count()
        user_pets = db.query(UserPet).filter(UserPet.user_id == user_id).count()

        total_animals = db.query(Animal).count()
        total_plants = db.query(Plant).count()
        total_tools = db.query(Tool).count()
        total_foods = db.query(Food).count()
        total_pets = db.query(Pet).count()

        collected_count = user_animals + user_plants + user_tools + user_foods + user_pets
        total_count = total_animals + total_plants + total_tools + total_foods + total_pets

        return UserProgress(
            user_id=user_id,
            collected_count=collected_count,
            total_count=total_count
        )
