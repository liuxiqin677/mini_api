from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Animal, Plant, Tool, Food
from app.models import UserAnimal, UserPlant, UserTool, UserFood


class LevelService:
    @staticmethod
    def calculate_level_from_progress(progress: float) -> int:
        if progress >= 80:
            return 5
        elif progress >= 60:
            return 4
        elif progress >= 40:
            return 3
        elif progress >= 20:
            return 2
        else:
            return 1

    @staticmethod
    def get_total_collection_progress(db: Session, user_id: int) -> float:
        total_animals = db.query(func.count(Animal.id)).scalar() or 0
        total_plants = db.query(func.count(Plant.id)).scalar() or 0
        total_tools = db.query(func.count(Tool.id)).scalar() or 0
        total_foods = db.query(func.count(Food.id)).scalar() or 0
        total = total_animals + total_plants + total_tools + total_foods

        if total == 0:
            return 0.0

        collected_animals = db.query(func.count(func.distinct(UserAnimal.animal_id))).filter(
            UserAnimal.user_id == user_id
        ).scalar() or 0
        collected_plants = db.query(func.count(func.distinct(UserPlant.plant_id))).filter(
            UserPlant.user_id == user_id
        ).scalar() or 0
        collected_tools = db.query(func.count(func.distinct(UserTool.tool_id))).filter(
            UserTool.user_id == user_id
        ).scalar() or 0
        collected_foods = db.query(func.count(func.distinct(UserFood.food_id))).filter(
            UserFood.user_id == user_id
        ).scalar() or 0
        collected = collected_animals + collected_plants + collected_tools + collected_foods

        return (collected / total) * 100

    @staticmethod
    def update_user_level(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        progress = LevelService.get_total_collection_progress(db, user_id)
        new_level = LevelService.calculate_level_from_progress(progress)

        if user.level != new_level:
            user.level = new_level
            db.commit()
            db.refresh(user)

        return user
