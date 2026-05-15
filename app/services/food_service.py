from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models import Food, UserFood
from app.schemas import FoodResponse, FoodDetail, UserFoodResponse, UserFoodWithDetail, UserFoodCollectionResponse


class FoodService:
    @staticmethod
    def get_all_foods(db: Session, user_id: int) -> List[FoodResponse]:
        foods = db.query(Food).all()
        user_collected_ids = {uf.food_id for uf in db.query(UserFood.food_id).filter(UserFood.user_id == user_id).all()}

        result = []
        for food in foods:
            result.append(FoodResponse(
                id=food.id,
                name=food.name,
                emoji=food.emoji,
                description=food.description,
                rarity=food.rarity,
                is_collected=food.id in user_collected_ids,
                world_ids=food.world_ids,
                target_ids=food.target_ids,
                created_at=food.created_at,
                updated_at=food.updated_at
            ))
        return result

    @staticmethod
    def get_food_by_id(db: Session, food_id: int, user_id: int) -> Optional[FoodDetail]:
        food = db.query(Food).filter(Food.id == food_id).first()
        if not food:
            return None

        user_collected = db.query(UserFood).filter(
            UserFood.user_id == user_id,
            UserFood.food_id == food_id
        ).first()

        return FoodDetail(
            id=food.id,
            name=food.name,
            emoji=food.emoji,
            description=food.description,
            rarity=food.rarity,
            is_collected=user_collected is not None,
            world_ids=food.world_ids,
            target_ids=food.target_ids,
            created_at=food.created_at,
            updated_at=food.updated_at
        )

    @staticmethod
    def collect_food(db: Session, user_id: int, food_id: int) -> Optional[UserFood]:
        food = db.query(Food).filter(Food.id == food_id).first()
        if not food:
            return None

        # 检查用户是否已经收集过这个食物
        user_food = db.query(UserFood).filter(
            UserFood.user_id == user_id,
            UserFood.food_id == food_id
        ).first()

        if user_food:
            # 如果已经收集过，数量+1
            user_food.count += 1
            db.commit()
            db.refresh(user_food)
            return user_food
        else:
            # 如果没有收集过，创建新记录
            user_food = UserFood(
                user_id=user_id,
                food_id=food_id,
                name=food.name,
                description=food.description,
                rarity=food.rarity,
                count=1
            )
            db.add(user_food)
            db.commit()
            db.refresh(user_food)
            return user_food

    @staticmethod
    def get_user_foods(db: Session, user_id: int) -> List[UserFoodResponse]:
        user_foods = db.query(UserFood).filter(UserFood.user_id == user_id).all()
        food_ids = [uf.food_id for uf in user_foods]
        foods = db.query(Food).filter(Food.id.in_(food_ids)).all()
        food_map = {f.id: f for f in foods}

        result = []
        for uf in user_foods:
            food = food_map.get(uf.food_id)
            emoji = food.emoji if food else ""
            result.append(UserFoodResponse(
                id=uf.id,
                user_id=uf.user_id,
                food_id=uf.food_id,
                name=uf.name,
                emoji=emoji,
                description=uf.description,
                rarity=uf.rarity,
                count=uf.count,
                created_at=uf.created_at,
                updated_at=uf.updated_at
            ))
        return result

    @staticmethod
    def get_user_foods_with_detail(db: Session, user_id: int) -> Tuple[List[UserFoodWithDetail], int]:
        """获取用户收集的食物列表，包含食物详情和数量"""
        user_foods = db.query(UserFood).filter(UserFood.user_id == user_id).all()
        food_ids = [uf.food_id for uf in user_foods]
        foods = db.query(Food).filter(Food.id.in_(food_ids)).all()
        food_map = {f.id: f for f in foods}

        result = []
        for uf in user_foods:
            food = food_map.get(uf.food_id)
            if food:
                food_response = FoodResponse(
                    id=food.id,
                    name=food.name,
                    emoji=food.emoji,
                    description=food.description,
                    rarity=food.rarity,
                    is_collected=True,
                    world_ids=food.world_ids,
                    target_ids=food.target_ids,
                    created_at=food.created_at,
                    updated_at=food.updated_at
                )
                result.append(UserFoodWithDetail(
                    id=uf.id,
                    user_id=uf.user_id,
                    food_id=uf.food_id,
                    name=uf.name,
                    emoji=food.emoji,
                    description=uf.description,
                    rarity=uf.rarity,
                    count=uf.count,
                    food_detail=food_response,
                    created_at=uf.created_at,
                    updated_at=uf.updated_at
                ))

        return result, len(result)

    @staticmethod
    def edit_food_name(db: Session, user_food_id: int, user_id: int, name: str) -> Optional[UserFood]:
        user_food = db.query(UserFood).filter(
            UserFood.id == user_food_id,
            UserFood.user_id == user_id
        ).first()
        if not user_food:
            return None

        user_food.name = name
        db.commit()
        db.refresh(user_food)
        return user_food

    @staticmethod
    def delete_food(db: Session, user_food_id: int, user_id: int) -> bool:
        user_food = db.query(UserFood).filter(
            UserFood.id == user_food_id,
            UserFood.user_id == user_id
        ).first()
        if not user_food:
            return False

        db.delete(user_food)
        db.commit()
        return True
