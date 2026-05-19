from typing import Optional, Dict
from sqlalchemy.orm import Session
from app.models import UserAnimal, UserPlant, Footprint
from app.schemas import UserAnimalResponse, UserPlantResponse


# 定义不同操作对应的好感度增长值
LOVE_INCREMENT: Dict[str, int] = {
    "feed": 5,         # 喂食增长 5
    "pet": 3,          # 抚摸增长 3
    "water": 4,        # 浇水增长 4
    "fertilize": 6     # 施肥增长 6
}

# 操作名称映射
ACTION_NAMES: Dict[str, str] = {
    "feed": "喂食",
    "pet": "抚摸",
    "water": "浇水",
    "fertilize": "施肥"
}


class NurtureService:
    @staticmethod
    def _create_footprint(
        db: Session,
        user_id: int,
        action_type: str,
        target_type: str,
        target_id: int,
        target_name: str,
        change_value: int
    ):
        """创建足迹记录"""
        footprint = Footprint(
            user_id=user_id,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            target_name=target_name,
            detail=f"对 {target_name} 进行了 {ACTION_NAMES[action_type]} 操作，好感度 +{change_value}",
            change_value=change_value
        )
        db.add(footprint)
        db.commit()

    @staticmethod
    def nurture_animal(
        db: Session,
        user_id: int,
        animal_id: int,
        action_type: str
    ) -> Optional[UserAnimal]:
        """培养动物"""
        # 验证操作类型
        if action_type not in ["feed", "pet"]:
            return None

        # 查询用户的动物
        user_animal = db.query(UserAnimal).filter(
            UserAnimal.user_id == user_id,
            UserAnimal.animal_id == animal_id
        ).first()

        if not user_animal:
            return None

        # 获取增长值
        increment = LOVE_INCREMENT.get(action_type, 1)

        # 更新好感度
        user_animal.love += increment
        db.commit()
        db.refresh(user_animal)

        # 记录足迹
        NurtureService._create_footprint(
            db, user_id, action_type, "animal", animal_id, user_animal.name, increment
        )

        return user_animal

    @staticmethod
    def nurture_plant(
        db: Session,
        user_id: int,
        plant_id: int,
        action_type: str
    ) -> Optional[UserPlant]:
        """培养植物"""
        # 验证操作类型
        if action_type not in ["water", "fertilize"]:
            return None

        # 查询用户的植物
        user_plant = db.query(UserPlant).filter(
            UserPlant.user_id == user_id,
            UserPlant.plant_id == plant_id
        ).first()

        if not user_plant:
            return None

        # 获取增长值
        increment = LOVE_INCREMENT.get(action_type, 1)

        # 更新好感度
        user_plant.love += increment
        db.commit()
        db.refresh(user_plant)

        # 记录足迹
        NurtureService._create_footprint(
            db, user_id, action_type, "plant", plant_id, user_plant.name, increment
        )

        return user_plant
