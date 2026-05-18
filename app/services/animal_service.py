from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Animal, UserAnimal, Food, Tool
from app.schemas import AnimalResponse, AnimalDetail, UserAnimalResponse
from app.schemas.food import FoodResponse
from app.schemas.tool import ToolResponse
from app.services.level_service import LevelService


class AnimalService:
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
    def get_animals_by_category(db: Session, category: str, user_id: int) -> List[AnimalResponse]:
        animals = db.query(Animal).filter(Animal.category == category).all()
        user_collected_ids = {ua.animal_id for ua in db.query(UserAnimal.animal_id).filter(UserAnimal.user_id == user_id).all()}

        result = []
        for animal in animals:
            foods = AnimalService._get_foods_by_ids(db, animal.favorite_food_ids)
            tools = AnimalService._get_tools_by_ids(db, animal.tool_ids)
            result.append(AnimalResponse(
                id=animal.id,
                name=animal.name,
                emoji=animal.emoji,
                description=animal.description,
                rarity=animal.rarity,
                category=animal.category,
                is_collected=animal.id in user_collected_ids,
                favorite_food_ids=animal.favorite_food_ids,
                tool_ids=animal.tool_ids,
                world_ids=animal.world_ids,
                foods=foods,
                tools=tools,
                created_at=animal.created_at,
                updated_at=animal.updated_at
            ))
        return result

    @staticmethod
    def get_animal_by_id(db: Session, animal_id: int, user_id: int) -> Optional[AnimalDetail]:
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if not animal:
            return None

        user_collected = db.query(UserAnimal).filter(
            UserAnimal.user_id == user_id,
            UserAnimal.animal_id == animal_id
        ).first()

        foods = AnimalService._get_foods_by_ids(db, animal.favorite_food_ids)
        tools = AnimalService._get_tools_by_ids(db, animal.tool_ids)

        return AnimalDetail(
            id=animal.id,
            name=animal.name,
            emoji=animal.emoji,
            description=animal.description,
            rarity=animal.rarity,
            category=animal.category,
            is_collected=user_collected is not None,
            favorite_food_ids=animal.favorite_food_ids,
                tool_ids=animal.tool_ids,
                world_ids=animal.world_ids,
                foods=foods,
                tools=tools,
                created_at=animal.created_at,
                updated_at=animal.updated_at
        )

    @staticmethod
    def collect_animal(db: Session, user_id: int, animal_id: int) -> Optional[UserAnimal]:
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if not animal:
            return None

        user_animal = UserAnimal(
            user_id=user_id,
            animal_id=animal_id,
            name=animal.name,
            description=animal.description,
            rarity=animal.rarity
        )
        db.add(user_animal)
        db.commit()
        db.refresh(user_animal)

        LevelService.update_user_level(db, user_id)

        return user_animal

    @staticmethod
    def get_user_animals(db: Session, user_id: int) -> List[UserAnimalResponse]:
        # Join with Animal table to get emoji and original name
        user_animals = db.query(UserAnimal, Animal).join(
            Animal, UserAnimal.animal_id == Animal.id
        ).filter(UserAnimal.user_id == user_id).all()

        result = []
        for ua, animal in user_animals:
            foods = AnimalService._get_foods_by_ids(db, animal.favorite_food_ids)
            tools = AnimalService._get_tools_by_ids(db, animal.tool_ids)
            result.append(UserAnimalResponse(
                id=ua.id,
                user_id=ua.user_id,
                animal_id=ua.animal_id,
                name=ua.name,
                original_name=animal.name,
                emoji=animal.emoji,
                description=ua.description,
                rarity=ua.rarity,
                favorite_food_ids=animal.favorite_food_ids,
                tool_ids=animal.tool_ids,
                foods=foods,
                tools=tools,
                created_at=ua.created_at,
                updated_at=ua.updated_at
            ))
        return result

    @staticmethod
    def edit_animal_name(db: Session, user_animal_id: int, user_id: int, name: str) -> Optional[UserAnimal]:
        user_animal = db.query(UserAnimal).filter(
            UserAnimal.id == user_animal_id,
            UserAnimal.user_id == user_id
        ).first()
        if not user_animal:
            return None

        user_animal.name = name
        db.commit()
        db.refresh(user_animal)
        return user_animal

    @staticmethod
    def delete_animal(db: Session, user_animal_id: int, user_id: int) -> bool:
        user_animal = db.query(UserAnimal).filter(
            UserAnimal.id == user_animal_id,
            UserAnimal.user_id == user_id
        ).first()
        if not user_animal:
            return False

        db.delete(user_animal)
        db.commit()
        return True
