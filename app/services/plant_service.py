from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Plant, UserPlant, Food, Tool
from app.schemas import PlantResponse, PlantDetail, UserPlantResponse
from app.schemas.food import FoodResponse
from app.schemas.tool import ToolResponse
from app.services.level_service import LevelService


class PlantService:
    @staticmethod
    def _get_foods_by_ids(db: Session, ids: Optional[List[int]]) -> List[FoodResponse]:
        """根据 ID 列表获取食物列表"""
        if not ids:
            return []

        foods = db.query(Food).filter(Food.id.in_(ids)).all()
        result = []
        for food in foods:
            result.append(FoodResponse(
                id=food.id,
                name=food.name,
                emoji=food.emoji,
                description=food.description,
                rarity=food.rarity,
                is_collected=False,
                world_ids=food.world_ids,
                target_ids=food.target_ids,
                created_at=food.created_at,
                updated_at=food.updated_at
            ))
        # 按照原始 ids 的顺序排序
        id_to_item = {item.id: item for item in result}
        sorted_result = []
        for item_id in ids:
            if item_id in id_to_item:
                sorted_result.append(id_to_item[item_id])
        return sorted_result

    @staticmethod
    def _get_tools_by_ids(db: Session, ids: Optional[List[int]]) -> List[ToolResponse]:
        """根据 ID 列表获取工具列表"""
        if not ids:
            return []

        tools = db.query(Tool).filter(Tool.id.in_(ids)).all()
        result = []
        for tool in tools:
            result.append(ToolResponse(
                id=tool.id,
                name=tool.name,
                emoji=tool.emoji,
                description=tool.description,
                rarity=tool.rarity,
                is_collected=False,
                world_ids=tool.world_ids,
                target_ids=tool.target_ids,
                created_at=tool.created_at,
                updated_at=tool.updated_at
            ))
        # 按照原始 ids 的顺序排序
        id_to_item = {item.id: item for item in result}
        sorted_result = []
        for item_id in ids:
            if item_id in id_to_item:
                sorted_result.append(id_to_item[item_id])
        return sorted_result

    @staticmethod
    def get_all_plants(db: Session, user_id: int) -> List[PlantResponse]:
        plants = db.query(Plant).all()
        user_collected_ids = {up.plant_id for up in db.query(UserPlant.plant_id).filter(UserPlant.user_id == user_id).all()}

        result = []
        for plant in plants:
            foods = PlantService._get_foods_by_ids(db, plant.favorite_food_ids)
            tools = PlantService._get_tools_by_ids(db, plant.tool_ids)
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
                foods=foods,
                tools=tools,
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

        foods = PlantService._get_foods_by_ids(db, plant.favorite_food_ids)
        tools = PlantService._get_tools_by_ids(db, plant.tool_ids)

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
            foods=foods,
            tools=tools,
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

        LevelService.update_user_level(db, user_id)

        return user_plant

    @staticmethod
    def get_user_plants(db: Session, user_id: int) -> List[UserPlantResponse]:
        # Join with Plant table to get emoji and original name
        user_plants = db.query(UserPlant, Plant).join(
            Plant, UserPlant.plant_id == Plant.id
        ).filter(UserPlant.user_id == user_id).all()

        result = []
        for up, plant in user_plants:
            foods = PlantService._get_foods_by_ids(db, plant.favorite_food_ids)
            tools = PlantService._get_tools_by_ids(db, plant.tool_ids)
            result.append(UserPlantResponse(
                id=up.id,
                user_id=up.user_id,
                plant_id=up.plant_id,
                name=up.name,
                original_name=plant.name,
                emoji=plant.emoji,
                description=up.description,
                rarity=up.rarity,
                favorite_food_ids=plant.favorite_food_ids,
                tool_ids=plant.tool_ids,
                foods=foods,
                tools=tools,
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
