from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Plant, UserPlant
from app.schemas import PlantResponse, PlantDetail, UserPlantResponse


class PlantService:
    @staticmethod
    def get_all_plants(db: Session, user_id: int) -> List[PlantResponse]:
        plants = db.query(Plant).all()
        user_collected_ids = {up.plant_id for up in db.query(UserPlant.plant_id).filter(UserPlant.user_id == user_id).all()}

        result = []
        for plant in plants:
            result.append(PlantResponse(
                id=plant.id,
                name=plant.name,
                emoji=plant.emoji,
                description=plant.description,
                rarity=plant.rarity,
                is_collected=plant.id in user_collected_ids,
                favorite_food_ids=plant.favorite_food_ids,
                tool_ids=plant.tool_ids,
                world_ids=plant.world_ids,
                created_at=plant.created_at,
                updated_at=plant.updated_at
            ))
        return result

    @staticmethod
    def get_plant_by_id(db: Session, plant_id: int, user_id: int) -> Optional[PlantDetail]:
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            return None

        user_collected = db.query(UserPlant).filter(
            UserPlant.user_id == user_id,
            UserPlant.plant_id == plant_id
        ).first()

        return PlantDetail(
            id=plant.id,
            name=plant.name,
            emoji=plant.emoji,
            description=plant.description,
            rarity=plant.rarity,
            is_collected=user_collected is not None,
            favorite_food_ids=plant.favorite_food_ids,
            tool_ids=plant.tool_ids,
            world_ids=plant.world_ids,
            created_at=plant.created_at,
            updated_at=plant.updated_at
        )

    @staticmethod
    def collect_plant(db: Session, user_id: int, plant_id: int) -> Optional[UserPlant]:
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            return None

        user_plant = UserPlant(
            user_id=user_id,
            plant_id=plant_id,
            name=plant.name,
            description=plant.description,
            rarity=plant.rarity
        )
        db.add(user_plant)
        db.commit()
        db.refresh(user_plant)
        return user_plant

    @staticmethod
    def get_user_plants(db: Session, user_id: int) -> List[UserPlantResponse]:
        user_plants = db.query(UserPlant).filter(UserPlant.user_id == user_id).all()
        result = []
        for up in user_plants:
            result.append(UserPlantResponse(
                id=up.id,
                user_id=up.user_id,
                plant_id=up.plant_id,
                name=up.name,
                description=up.description,
                rarity=up.rarity,
                created_at=up.created_at,
                updated_at=up.updated_at
            ))
        return result

    @staticmethod
    def edit_plant_name(db: Session, user_plant_id: int, user_id: int, name: str) -> Optional[UserPlant]:
        user_plant = db.query(UserPlant).filter(
            UserPlant.id == user_plant_id,
            UserPlant.user_id == user_id
        ).first()
        if not user_plant:
            return None

        user_plant.name = name
        db.commit()
        db.refresh(user_plant)
        return user_plant

    @staticmethod
    def delete_plant(db: Session, user_plant_id: int, user_id: int) -> bool:
        user_plant = db.query(UserPlant).filter(
            UserPlant.id == user_plant_id,
            UserPlant.user_id == user_id
        ).first()
        if not user_plant:
            return False

        db.delete(user_plant)
        db.commit()
        return True
