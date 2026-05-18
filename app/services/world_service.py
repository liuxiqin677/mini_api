from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import World, Animal, Plant, Tool, Food
from app.schemas import WorldResponse, WorldDetail
from app.schemas.animal import AnimalResponse
from app.schemas.plant import PlantResponse
from app.schemas.tool import ToolResponse
from app.schemas.food import FoodResponse


class WorldService:
    @staticmethod
    def get_all_worlds(db: Session) -> List[WorldResponse]:
        worlds = db.query(World).all()
        result = []
        for world in worlds:
            result.append(WorldResponse(
                id=world.id,
                name=world.name,
                emoji=world.emoji,
                description=world.description,
                bg_color=world.bg_color,
                gradient=world.gradient,
                animal_ids=world.animal_ids,
                plant_ids=world.plant_ids,
                tool_ids=world.tool_ids,
                food_ids=world.food_ids,
                created_at=world.created_at,
                updated_at=world.updated_at
            ))
        return result

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
    def _get_tools_by_ids_for_detail(db: Session, ids: Optional[List[int]]) -> List[ToolResponse]:
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
    def _get_animals_by_ids(db: Session, ids: Optional[List[int]]) -> List[AnimalResponse]:
        """根据 ID 列表获取动物列表"""
        if not ids:
            return []

        animals = db.query(Animal).filter(Animal.id.in_(ids)).all()
        result = []
        for animal in animals:
            foods = WorldService._get_foods_by_ids(db, animal.favorite_food_ids)
            tools = WorldService._get_tools_by_ids_for_detail(db, animal.tool_ids)
            result.append(AnimalResponse(
                id=animal.id,
                name=animal.name,
                emoji=animal.emoji,
                description=animal.description,
                rarity=animal.rarity,
                category=animal.category,
                is_collected=False,
                favorite_food_ids=animal.favorite_food_ids,
                tool_ids=animal.tool_ids,
                world_ids=animal.world_ids,
                foods=foods,
                tools=tools,
                created_at=animal.created_at,
                updated_at=animal.updated_at
            ))
        # 按照原始 ids 的顺序排序
        id_to_item = {item.id: item for item in result}
        sorted_result = []
        for item_id in ids:
            if item_id in id_to_item:
                sorted_result.append(id_to_item[item_id])
        return sorted_result

    @staticmethod
    def _get_plants_by_ids(db: Session, ids: Optional[List[int]]) -> List[PlantResponse]:
        """根据 ID 列表获取植物列表"""
        if not ids:
            return []

        plants = db.query(Plant).filter(Plant.id.in_(ids)).all()
        result = []
        for plant in plants:
            foods = WorldService._get_foods_by_ids(db, plant.favorite_food_ids)
            tools = WorldService._get_tools_by_ids_for_detail(db, plant.tool_ids)
            result.append(PlantResponse(
                id=plant.id,
                name=plant.name,
                emoji=plant.emoji,
                description=plant.description,
                rarity=plant.rarity,
                is_collected=False,
                favorite_food_ids=plant.favorite_food_ids,
                tool_ids=plant.tool_ids,
                world_ids=plant.world_ids,
                foods=foods,
                tools=tools,
                created_at=plant.created_at,
                updated_at=plant.updated_at
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
    def get_world_by_id(db: Session, world_id: int) -> Optional[WorldDetail]:
        world = db.query(World).filter(World.id == world_id).first()
        if not world:
            return None

        # 获取详细信息
        animals = WorldService._get_animals_by_ids(db, world.animal_ids)
        plants = WorldService._get_plants_by_ids(db, world.plant_ids)
        tools = WorldService._get_tools_by_ids(db, world.tool_ids)
        foods = WorldService._get_foods_by_ids(db, world.food_ids)

        return WorldDetail(
            id=world.id,
            name=world.name,
            emoji=world.emoji,
            description=world.description,
            bg_color=world.bg_color,
            gradient=world.gradient,
            animal_ids=world.animal_ids,
            plant_ids=world.plant_ids,
            tool_ids=world.tool_ids,
            food_ids=world.food_ids,
            animals=animals,
            plants=plants,
            tools=tools,
            foods=foods,
            created_at=world.created_at,
            updated_at=world.updated_at
        )
