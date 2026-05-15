from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Animal, Plant, Tool, Food
from app.models import UserAnimal, UserPlant, UserTool, UserFood
from app.schemas import CollectionProgressItem, CollectionProgressResponse


class CollectionService:
    @staticmethod
    def get_collection_progress(db: Session, user_id: int) -> CollectionProgressResponse:
        """获取用户的图鉴收集进度"""
        items: List[CollectionProgressItem] = []

        # 1. 处理动物 - 按分类分组
        # 获取所有动物分类
        animal_categories = db.query(Animal.category).distinct().all()
        categories = [cat[0] for cat in animal_categories if cat[0]]

        # 分类与emoji、名称、描述、背景色的映射
        category_info = {
            'mammal': ('哺乳动物', '🦁', '温血脊椎动物', '#FFF5E6'),
            'bird': ('鸟类', '🦅', '会飞的羽毛朋友', '#F0F9FF'),
            'reptile': ('爬行动物', '🦎', '冷血爬生物', '#F0FDF4'),
            'ocean': ('海洋生物', '🐋', '深海神秘生物', '#EEF2FF'),
            'wildlife': ('野生动物', '🦊', '荒野中的猎手', '#FDF4FF'),
        }

        for category in categories:
            # 获取该分类的总动物数
            total_animals = db.query(func.count(Animal.id)).filter(
                Animal.category == category
            ).scalar() or 0

            # 获取用户在该分类收集的动物数（去重）
            collected_animals = db.query(func.count(func.distinct(UserAnimal.animal_id))).join(
                Animal, UserAnimal.animal_id == Animal.id
            ).filter(
                UserAnimal.user_id == user_id,
                Animal.category == category
            ).scalar() or 0

            # 计算进度
            progress = int((collected_animals / total_animals * 100)) if total_animals > 0 else 0

            # 获取该分类的展示信息
            name, emoji, description, bg_color = category_info.get(category, (category, '❓', '', '#F5F5F5'))

            items.append(CollectionProgressItem(
                id=f'animal_{category}',
                name=name,
                emoji=emoji,
                collected_count=collected_animals,
                total_count=total_animals,
                progress=progress,
                bg_color=bg_color,
                description=description
            ))

        # 2. 处理植物
        total_plants = db.query(func.count(Plant.id)).scalar() or 0
        collected_plants = db.query(func.count(func.distinct(UserPlant.plant_id))).filter(
            UserPlant.user_id == user_id
        ).scalar() or 0
        plant_progress = int((collected_plants / total_plants * 100)) if total_plants > 0 else 0

        items.append(CollectionProgressItem(
            id='plants',
            name='植物',
            emoji='🌸',
            collected_count=collected_plants,
            total_count=total_plants,
            progress=plant_progress,
            bg_color='#FFF1F2',
            description='美丽的植物世界'
        ))

        # 3. 处理工具
        total_tools = db.query(func.count(Tool.id)).scalar() or 0
        collected_tools = db.query(func.count(func.distinct(UserTool.tool_id))).filter(
            UserTool.user_id == user_id
        ).scalar() or 0
        tool_progress = int((collected_tools / total_tools * 100)) if total_tools > 0 else 0

        items.append(CollectionProgressItem(
            id='tools',
            name='工具',
            emoji='🔧',
            collected_count=collected_tools,
            total_count=total_tools,
            progress=tool_progress,
            bg_color='#F5F5F5',
            description='有用的工具'
        ))

        # 4. 处理食物
        total_foods = db.query(func.count(Food.id)).scalar() or 0
        collected_foods = db.query(func.count(func.distinct(UserFood.food_id))).filter(
            UserFood.user_id == user_id
        ).scalar() or 0
        food_progress = int((collected_foods / total_foods * 100)) if total_foods > 0 else 0

        items.append(CollectionProgressItem(
            id='foods',
            name='食物',
            emoji='🍎',
            collected_count=collected_foods,
            total_count=total_foods,
            progress=food_progress,
            bg_color='#FFF8F0',
            description='有用的饲料'
        ))

        return CollectionProgressResponse(items=items)
