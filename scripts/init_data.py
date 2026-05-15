import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Animal, Plant, Tool, Food, Pet, World
from sqlalchemy.orm import Session

# 动物数据
ANIMALS_DATA = [
    {"name": "猴子", "emoji": "🐒", "description": "灵活的攀爬者", "rarity": "common", "category": "mammal", "world_ids": [1]},
    {"name": "大猩猩", "emoji": "🦍", "description": "强壮的灵长类", "rarity": "rare", "category": "mammal", "world_ids": [1]},
    {"name": "狮子", "emoji": "🦁", "description": "草原之王", "rarity": "rare", "category": "mammal", "world_ids": [1, 5]},
    {"name": "老虎", "emoji": "🐯", "description": "森林霸主", "rarity": "epic", "category": "mammal", "world_ids": [5]},
    {"name": "大象", "emoji": "🐘", "description": "陆地最大动物", "rarity": "rare", "category": "mammal", "world_ids": [1]},
    {"name": "熊猫", "emoji": "🐼", "description": "国宝级动物", "rarity": "legendary", "category": "mammal", "world_ids": [5]},
    {"name": "狼", "emoji": "🐺", "description": "荒野中的猎手", "rarity": "rare", "category": "wildlife", "world_ids": [5]},
    {"name": "狐狸", "emoji": "🦊", "description": "狡猾的精灵", "rarity": "common", "category": "wildlife", "world_ids": [5]},
    {"name": "鹰", "emoji": "🦅", "description": "天空猎手", "rarity": "rare", "category": "bird", "world_ids": [2]},
    {"name": "鹦鹉", "emoji": "🦜", "description": "会说话的鸟", "rarity": "common", "category": "bird", "world_ids": [2]},
    {"name": "孔雀", "emoji": "🦚", "description": "美丽的尾羽", "rarity": "epic", "category": "bird", "world_ids": [2]},
    {"name": "猫头鹰", "emoji": "🦉", "description": "夜间猎手", "rarity": "rare", "category": "bird", "world_ids": [2]},
    {"name": "蜥蜴", "emoji": "🦎", "description": "灵巧的小爬虫", "rarity": "common", "category": "reptile", "world_ids": [3]},
    {"name": "蛇", "emoji": "🐍", "description": "神秘的爬行者", "rarity": "rare", "category": "reptile", "world_ids": [3]},
    {"name": "鳄鱼", "emoji": "🐊", "description": "水中霸主", "rarity": "epic", "category": "reptile", "world_ids": [3, 4]},
    {"name": "海豚", "emoji": "🐬", "description": "海洋精灵", "rarity": "rare", "category": "ocean", "world_ids": [4]},
    {"name": "鲸鱼", "emoji": "🐋", "description": "海洋巨无霸", "rarity": "epic", "category": "ocean", "world_ids": [4]},
    {"name": "鲨鱼", "emoji": "🦈", "description": "海洋猎手", "rarity": "rare", "category": "ocean", "world_ids": [4]},
    {"name": "章鱼", "emoji": "🐙", "description": "八条腿的智者", "rarity": "legendary", "category": "ocean", "world_ids": [4]},
]

# 植物数据
PLANTS_DATA = [
    {"name": "樱花", "emoji": "🌸", "description": "春日之花", "rarity": "common", "world_ids": [6]},
    {"name": "玫瑰", "emoji": "🌹", "description": "爱情之花", "rarity": "rare", "world_ids": [6]},
    {"name": "向日葵", "emoji": "🌻", "description": "阳光的追随者", "rarity": "common", "world_ids": [6]},
    {"name": "仙人掌", "emoji": "🌵", "description": "沙漠中的勇士", "rarity": "common", "world_ids": [6]},
    {"name": "四叶草", "emoji": "🍀", "description": "幸运的象征", "rarity": "legendary", "world_ids": [6]},
    {"name": "郁金香", "emoji": "🌷", "description": "优雅的花朵", "rarity": "rare", "world_ids": [6]},
    {"name": "百合", "emoji": "💐", "description": "纯洁的象征", "rarity": "epic", "world_ids": [6]},
]

# 工具数据
TOOLS_DATA = [
    {"name": "望远镜", "emoji": "🔭", "description": "观察远处的生物", "rarity": "common", "world_ids": [1, 2, 5]},
    {"name": "网", "emoji": "🥅", "description": "捕捉工具", "rarity": "common", "world_ids": [1, 2, 3, 4]},
    {"name": "收集篮", "emoji": "🧺", "description": "收集物品", "rarity": "common", "world_ids": [6]},
    {"name": "潜水镜", "emoji": "🤿", "description": "海底探索", "rarity": "rare", "world_ids": [4]},
    {"name": "登山靴", "emoji": "🥾", "description": "野外探险", "rarity": "rare", "world_ids": [5]},
    {"name": "神秘罗盘", "emoji": "🧭", "description": "指向稀有生物", "rarity": "epic", "world_ids": [1, 2, 3, 4, 5, 6]},
]

# 食物/饲料数据
FOODS_DATA = [
    {"name": "肉", "emoji": "🥩", "description": "肉食动物喜欢", "rarity": "common", "world_ids": [1, 3, 5]},
    {"name": "鱼", "emoji": "🐟", "description": "海洋生物喜欢", "rarity": "common", "world_ids": [4]},
    {"name": "坚果", "emoji": "🥜", "description": "小动物喜欢", "rarity": "common", "world_ids": [1, 2, 5]},
    {"name": "水果", "emoji": "🍎", "description": "很多动物喜欢", "rarity": "common", "world_ids": [1, 5]},
    {"name": "蜂蜜", "emoji": "🍯", "description": "熊类最爱", "rarity": "rare", "world_ids": [1, 5]},
    {"name": "特殊饲料", "emoji": "✨", "description": "稀有生物喜欢", "rarity": "legendary", "world_ids": [1, 2, 3, 4, 5, 6]},
    {"name": "水", "emoji": "💧", "description": "所有生物都需要", "rarity": "common", "world_ids": [1, 2, 3, 4, 5, 6]},
    {"name": "阳光", "emoji": "☀️", "description": "植物的养料", "rarity": "common", "world_ids": [6]},
]

# 宠物数据
PETS_DATA = [
    {"name": "狗", "emoji": "🐕", "description": "人类最好的朋友", "rarity": "common", "world_ids": [1, 5]},
    {"name": "猫", "emoji": "🐈", "description": "高冷的小伙伴", "rarity": "common", "world_ids": [1, 5]},
    {"name": "仓鼠", "emoji": "🐹", "description": "可爱的小宠物", "rarity": "common", "world_ids": [1]},
    {"name": "兔子", "emoji": "🐰", "description": "蹦蹦跳跳的小可爱", "rarity": "common", "world_ids": [1, 5]},
    {"name": "龙猫", "emoji": "🐭", "description": "毛绒绒的小伙伴", "rarity": "rare", "world_ids": [5]},
]

# 世界数据
WORLDS_DATA = [
    {"name": "狂野陆地", "emoji": "🦁", "description": "探索草原与森林", "bg_color": "#FFF5E6", "gradient": "linear-gradient(135deg, #FFF5E6, #FFE4B5)"},
    {"name": "无限天空", "emoji": "🦅", "description": "翱翔云端之上", "bg_color": "#F0F9FF", "gradient": "linear-gradient(135deg, #F0F9FF, #B0E0E6)"},
    {"name": "诡异爬行", "emoji": "🦎", "description": "穿越阴暗洞穴", "bg_color": "#F0FDF4", "gradient": "linear-gradient(135deg, #F0FDF4, #C8E6C9)"},
    {"name": "傲慢海洋", "emoji": "🐬", "description": "深入神秘海底", "bg_color": "#EEF2FF", "gradient": "linear-gradient(135deg, #EEF2FF, #87CEEB)"},
    {"name": "荒芜荒野", "emoji": "🐺", "description": "征服荒漠戈壁", "bg_color": "#FDF4FF", "gradient": "linear-gradient(135deg, #FDF4FF, #E1BEE7)"},
    {"name": "密林花园", "emoji": "🌸", "description": "漫步丛林密园", "bg_color": "#FFF1F2", "gradient": "linear-gradient(135deg, #FFF1F2, #FFCDD2)"},
]


def init_db():
    """完整初始化数据库"""
    # 重新创建所有表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 初始化世界
        worlds = []
        for world_data in WORLDS_DATA:
            world = World(**world_data)
            db.add(world)
            worlds.append(world)
        db.flush()

        # 创建ID映射
        world_map = {w.name: w.id for w in worlds}

        # 直接使用数字作为world_ids，因为我们是按顺序创建世界的
        for animal_data in ANIMALS_DATA:
            animal = Animal(**animal_data)
            db.add(animal)

        for plant_data in PLANTS_DATA:
            plant = Plant(**plant_data)
            db.add(plant)

        for tool_data in TOOLS_DATA:
            tool = Tool(**tool_data)
            db.add(tool)

        for food_data in FOODS_DATA:
            food = Food(**food_data)
            db.add(food)

        for pet_data in PETS_DATA:
            pet = Pet(**pet_data)
            db.add(pet)

        # 刷新以获取ID
        db.flush()

        # 更新世界的关系数据
        all_animals = db.query(Animal).all()
        all_plants = db.query(Plant).all()
        all_tools = db.query(Tool).all()
        all_foods = db.query(Food).all()

        for world in worlds:
            world.animal_ids = [a.id for a in all_animals if world.id in (a.world_ids or [])]
            world.plant_ids = [p.id for p in all_plants if world.id in (p.world_ids or [])]
            world.tool_ids = [t.id for t in all_tools if world.id in (t.world_ids or [])]
            world.food_ids = [f.id for f in all_foods if world.id in (f.world_ids or [])]

        db.commit()

        print("Database initialized successfully!")
        print(f"{len(worlds)} worlds")
        print(f"{len(ANIMALS_DATA)} animals")
        print(f"{len(PLANTS_DATA)} plants")
        print(f"{len(TOOLS_DATA)} tools")
        print(f"{len(FOODS_DATA)} foods")
        print(f"{len(PETS_DATA)} pets")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
