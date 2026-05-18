#!/usr/bin/env python3
"""
数据库初始化脚本
使用方法：
    python init.py          # 完整初始化（删除旧库 + 初始化数据 + 测试API）
    python init.py --data   # 仅重新初始化数据（保留数据库结构）
    python init.py --test   # 仅测试API
"""

import os
import sys
import time
import argparse
from typing import Optional

# 确保在正确的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# ==========================================
# 初始化数据配置 - 在这里修改你的数据！
# ==========================================

# 世界数据
WORLDS_DATA = [
    {"name": "狂野陆地", "emoji": "🦁", "description": "探索草原与森林", "bg_color": "#FFF5E6", "gradient": "linear-gradient(135deg, #FFF5E6, #FFE4B5)"},
    {"name": "无限天空", "emoji": "🦅", "description": "翱翔云端之上", "bg_color": "#F0F9FF", "gradient": "linear-gradient(135deg, #F0F9FF, #B0E0E6)"},
    {"name": "诡异爬行", "emoji": "🦎", "description": "穿越阴暗洞穴", "bg_color": "#F0FDF4", "gradient": "linear-gradient(135deg, #F0FDF4, #C8E6C9)"},
    {"name": "傲慢海洋", "emoji": "🐬", "description": "深入神秘海底", "bg_color": "#EEF2FF", "gradient": "linear-gradient(135deg, #EEF2FF, #87CEEB)"},
    {"name": "荒芜荒野", "emoji": "🐺", "description": "征服荒漠戈壁", "bg_color": "#FDF4FF", "gradient": "linear-gradient(135deg, #FDF4FF, #E1BEE7)"},
    {"name": "密林花园", "emoji": "🌸", "description": "漫步丛林密园", "bg_color": "#FFF1F2", "gradient": "linear-gradient(135deg, #FFF1F2, #FFCDD2)"},
]

# 动物数据
ANIMALS_DATA = [
    {"name": "猴子", "emoji": "🐒", "description": "灵活的攀爬者", "rarity": "common", "category": "mammal", "world_ids": [1], "tool_ids": [1, 2], "favorite_food_ids": [3, 4]},
    {"name": "大猩猩", "emoji": "🦍", "description": "强壮的灵长类", "rarity": "rare", "category": "mammal", "world_ids": [1], "tool_ids": [2, 6], "favorite_food_ids": [3, 4, 5]},
    {"name": "狮子", "emoji": "🦁", "description": "草原之王", "rarity": "rare", "category": "mammal", "world_ids": [1, 5], "tool_ids": [1, 2, 5], "favorite_food_ids": [1, 5]},
    {"name": "老虎", "emoji": "🐯", "description": "森林霸主", "rarity": "epic", "category": "mammal", "world_ids": [5], "tool_ids": [1, 2, 5, 6], "favorite_food_ids": [1, 5, 6]},
    {"name": "大象", "emoji": "🐘", "description": "陆地最大动物", "rarity": "rare", "category": "mammal", "world_ids": [1], "tool_ids": [2, 5], "favorite_food_ids": [4, 7]},
    {"name": "熊猫", "emoji": "🐼", "description": "国宝级动物", "rarity": "legendary", "category": "mammal", "world_ids": [5], "tool_ids": [1, 2, 6], "favorite_food_ids": [3, 5, 6, 7]},
    {"name": "狼", "emoji": "🐺", "description": "荒野中的猎手", "rarity": "rare", "category": "wildlife", "world_ids": [5], "tool_ids": [1, 2, 5], "favorite_food_ids": [1, 3]},
    {"name": "狐狸", "emoji": "🦊", "description": "狡猾的精灵", "rarity": "common", "category": "wildlife", "world_ids": [5], "tool_ids": [1, 2], "favorite_food_ids": [1, 3, 4]},
    {"name": "鹰", "emoji": "🦅", "description": "天空猎手", "rarity": "rare", "category": "bird", "world_ids": [2], "tool_ids": [1, 6], "favorite_food_ids": [2, 3]},
    {"name": "鹦鹉", "emoji": "🦜", "description": "会说话的鸟", "rarity": "common", "category": "bird", "world_ids": [2], "tool_ids": [1, 2], "favorite_food_ids": [3, 4, 7]},
    {"name": "孔雀", "emoji": "🦚", "description": "美丽的尾羽", "rarity": "epic", "category": "bird", "world_ids": [2], "tool_ids": [1, 2, 6], "favorite_food_ids": [3, 5, 7]},
    {"name": "猫头鹰", "emoji": "🦉", "description": "夜间猎手", "rarity": "rare", "category": "bird", "world_ids": [2], "tool_ids": [1, 6], "favorite_food_ids": [2, 3]},
    {"name": "蜥蜴", "emoji": "🦎", "description": "灵巧的小爬虫", "rarity": "common", "category": "reptile", "world_ids": [3], "tool_ids": [2, 3], "favorite_food_ids": [3, 7]},
    {"name": "蛇", "emoji": "🐍", "description": "神秘的爬行者", "rarity": "rare", "category": "reptile", "world_ids": [3], "tool_ids": [2, 6], "favorite_food_ids": [1, 3]},
    {"name": "鳄鱼", "emoji": "🐊", "description": "水中霸主", "rarity": "epic", "category": "reptile", "world_ids": [3, 4], "tool_ids": [2, 4, 6], "favorite_food_ids": [1, 2, 5]},
    {"name": "海豚", "emoji": "🐬", "description": "海洋精灵", "rarity": "rare", "category": "ocean", "world_ids": [4], "tool_ids": [4, 6], "favorite_food_ids": [2, 5, 7]},
    {"name": "鲸鱼", "emoji": "🐋", "description": "海洋巨无霸", "rarity": "epic", "category": "ocean", "world_ids": [4], "tool_ids": [4, 6], "favorite_food_ids": [2, 6, 7]},
    {"name": "鲨鱼", "emoji": "🦈", "description": "海洋猎手", "rarity": "rare", "category": "ocean", "world_ids": [4], "tool_ids": [4, 6], "favorite_food_ids": [1, 2]},
    {"name": "章鱼", "emoji": "🐙", "description": "八条腿的智者", "rarity": "legendary", "category": "ocean", "world_ids": [4], "tool_ids": [2, 4, 6], "favorite_food_ids": [2, 3, 5, 6]},
]

# 植物数据
PLANTS_DATA = [
    {"name": "樱花", "emoji": "🌸", "description": "春日之花", "rarity": "common", "world_ids": [6], "tool_ids": [3, 6], "favorite_food_ids": [7, 8]},
    {"name": "玫瑰", "emoji": "🌹", "description": "爱情之花", "rarity": "rare", "world_ids": [6], "tool_ids": [3, 6], "favorite_food_ids": [7, 8, 5]},
    {"name": "向日葵", "emoji": "🌻", "description": "阳光的追随者", "rarity": "common", "world_ids": [6], "tool_ids": [3], "favorite_food_ids": [8, 7]},
    {"name": "仙人掌", "emoji": "🌵", "description": "沙漠中的勇士", "rarity": "common", "world_ids": [6], "tool_ids": [3, 5], "favorite_food_ids": [7, 8]},
    {"name": "四叶草", "emoji": "🍀", "description": "幸运的象征", "rarity": "legendary", "world_ids": [6], "tool_ids": [3, 6], "favorite_food_ids": [7, 8, 5, 6]},
    {"name": "郁金香", "emoji": "🌷", "description": "优雅的花朵", "rarity": "rare", "world_ids": [6], "tool_ids": [3, 6], "favorite_food_ids": [7, 8, 5]},
    {"name": "百合", "emoji": "💐", "description": "纯洁的象征", "rarity": "epic", "world_ids": [6], "tool_ids": [3, 6], "favorite_food_ids": [7, 8, 6]},
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

# 数据库文件路径
DB_FILE = "working.db"


def print_title(title: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_step(step: str, success: Optional[bool] = None):
    """打印步骤"""
    if success is True:
        print(f"  [OK] {step}")
    elif success is False:
        print(f"  [FAIL] {step}")
    else:
        print(f"  {step}")


def delete_old_database() -> bool:
    """删除旧数据库"""
    print_title("删除旧数据库")

    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print_step(f"删除数据库文件: {DB_FILE}", True)
            return True
        except Exception as e:
            print_step(f"无法删除 {DB_FILE}: {e}", False)
            return False
    else:
        print_step(f"数据库文件 {DB_FILE} 不存在，跳过删除", True)
        return True


def init_database_data():
    """初始化数据库数据"""
    print_title("初始化数据库")

    from app.database import engine, Base, SessionLocal
    from app.models import Animal, Plant, Tool, Food, Pet, World

    # 重新创建所有表
    print_step("删除旧表...")
    Base.metadata.drop_all(bind=engine)
    print_step("创建新表...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 初始化世界
        print_step("初始化世界数据...")
        worlds = []
        for world_data in WORLDS_DATA:
            world = World(**world_data)
            db.add(world)
            worlds.append(world)
        db.flush()
        print_step(f"创建了 {len(worlds)} 个世界", True)

        # 初始化动物
        print_step("初始化动物数据...")
        for animal_data in ANIMALS_DATA:
            animal = Animal(**animal_data)
            db.add(animal)
        print_step(f"创建了 {len(ANIMALS_DATA)} 个动物", True)

        # 初始化植物
        print_step("初始化植物数据...")
        for plant_data in PLANTS_DATA:
            plant = Plant(**plant_data)
            db.add(plant)
        print_step(f"创建了 {len(PLANTS_DATA)} 个植物", True)

        # 初始化工具
        print_step("初始化工具数据...")
        for tool_data in TOOLS_DATA:
            tool = Tool(**tool_data)
            db.add(tool)
        print_step(f"创建了 {len(TOOLS_DATA)} 个工具", True)

        # 初始化食物
        print_step("初始化食物数据...")
        for food_data in FOODS_DATA:
            food = Food(**food_data)
            db.add(food)
        print_step(f"创建了 {len(FOODS_DATA)} 个食物", True)

        # 初始化宠物
        print_step("初始化宠物数据...")
        for pet_data in PETS_DATA:
            pet = Pet(**pet_data)
            db.add(pet)
        print_step(f"创建了 {len(PETS_DATA)} 个宠物", True)

        # 刷新以获取ID
        db.flush()

        # 更新世界的关系数据
        print_step("更新世界关系数据...")
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
        print_step("数据提交成功！", True)

        print("\n数据统计:")
        print(f"  世界: {len(worlds)}")
        print(f"  动物: {len(ANIMALS_DATA)}")
        print(f"  植物: {len(PLANTS_DATA)}")
        print(f"  工具: {len(TOOLS_DATA)}")
        print(f"  食物: {len(FOODS_DATA)}")
        print(f"  宠物: {len(PETS_DATA)}")

        return True

    except Exception as e:
        db.rollback()
        print_step(f"初始化失败: {e}", False)
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_api() -> bool:
    """测试API接口"""
    print_title("测试API接口")

    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # 测试根路径
        print_step("测试根路径...")
        response = client.get("/")
        if response.status_code == 200:
            print_step("根路径正常", True)
        else:
            print_step(f"根路径异常: {response.status_code}", False)
            return False

        # 测试健康检查
        print_step("测试健康检查...")
        response = client.get("/health")
        if response.status_code == 200:
            print_step("健康检查正常", True)
        else:
            print_step(f"健康检查异常: {response.status_code}", False)
            return False

        # 测试登录（使用/user/login）
        print_step("测试登录...")
        response = client.post("/api/v1/user/login", json={"username": "testuser", "password": "testpass"})
        if response.status_code == 200:
            print_step("登录成功", True)
            data = response.json()
            token = data["data"]["access_token"]
            auth_headers = {"Authorization": f"Bearer {token}"}
        else:
            print_step(f"登录异常: {response.status_code}", False)
            return False

        # 测试获取用户详情
        print_step("测试获取用户详情...")
        response = client.get("/api/v1/user/detail", headers=auth_headers)
        if response.status_code == 200:
            print_step("获取用户详情成功", True)
        else:
            print_step(f"获取用户详情异常: {response.status_code}", False)

        # 测试获取用户进度
        print_step("测试获取用户进度...")
        response = client.get("/api/v1/user/collect/progress", headers=auth_headers)
        if response.status_code == 200:
            print_step("获取用户进度成功", True)
        else:
            print_step(f"获取用户进度异常: {response.status_code}", False)

        # 测试获取世界列表
        print_step("测试获取世界列表...")
        response = client.get("/api/v1/world/list", headers=auth_headers)
        if response.status_code == 200:
            worlds = response.json()["data"]
            print_step(f"获取到 {len(worlds)} 个世界", True)
        else:
            print_step(f"获取世界列表异常: {response.status_code}", False)
            return False

        # 测试获取哺乳动物列表
        print_step("测试获取哺乳动物列表...")
        response = client.get("/api/v1/mammals/animals/list", headers=auth_headers)
        if response.status_code == 200:
            animals = response.json()["data"]
            print_step(f"获取到 {len(animals)} 个哺乳动物", True)
        else:
            print_step(f"获取哺乳动物列表异常: {response.status_code}", False)

        # 测试获取鸟类列表
        print_step("测试获取鸟类列表...")
        response = client.get("/api/v1/birds/animals/list", headers=auth_headers)
        if response.status_code == 200:
            animals = response.json()["data"]
            print_step(f"获取到 {len(animals)} 个鸟类", True)
        else:
            print_step(f"获取鸟类列表异常: {response.status_code}", False)

        # 测试获取爬行动物列表
        print_step("测试获取爬行动物列表...")
        response = client.get("/api/v1/reptiles/animals/list", headers=auth_headers)
        if response.status_code == 200:
            animals = response.json()["data"]
            print_step(f"获取到 {len(animals)} 个爬行动物", True)
        else:
            print_step(f"获取爬行动物列表异常: {response.status_code}", False)

        # 测试获取海洋生物列表
        print_step("测试获取海洋生物列表...")
        response = client.get("/api/v1/ocean/animals/list", headers=auth_headers)
        if response.status_code == 200:
            animals = response.json()["data"]
            print_step(f"获取到 {len(animals)} 个海洋生物", True)
        else:
            print_step(f"获取海洋生物列表异常: {response.status_code}", False)

        # 测试获取野生动物列表
        print_step("测试获取野生动物列表...")
        response = client.get("/api/v1/wildlife/animals/list", headers=auth_headers)
        if response.status_code == 200:
            animals = response.json()["data"]
            print_step(f"获取到 {len(animals)} 个野生动物", True)
        else:
            print_step(f"获取野生动物列表异常: {response.status_code}", False)

        # 测试获取植物列表
        print_step("测试获取植物列表...")
        response = client.get("/api/v1/plants/animals/list", headers=auth_headers)
        if response.status_code == 200:
            plants = response.json()["data"]
            print_step(f"获取到 {len(plants)} 个植物", True)
        else:
            print_step(f"获取植物列表异常: {response.status_code}", False)

        # 测试获取工具列表
        print_step("测试获取工具列表...")
        response = client.get("/api/v1/tools/list", headers=auth_headers)
        if response.status_code == 200:
            tools = response.json()["data"]
            print_step(f"获取到 {len(tools)} 个工具", True)
        else:
            print_step(f"获取工具列表异常: {response.status_code}", False)

        # 测试获取食物列表
        print_step("测试获取食物列表...")
        response = client.get("/api/v1/foods/list", headers=auth_headers)
        if response.status_code == 200:
            foods = response.json()["data"]
            print_step(f"获取到 {len(foods)} 个食物", True)
        else:
            print_step(f"获取食物列表异常: {response.status_code}", False)

        # 测试收集工具
        print_step("测试收集工具...")
        if len(TOOLS_DATA) > 0:
            tool_id = 1
            response = client.post("/api/v1/user/collect/tool", json={"tool_id": tool_id}, headers=auth_headers)
            if response.status_code == 200:
                print_step("收集工具成功", True)
                # 再次收集，测试数量+1
                response = client.post("/api/v1/user/collect/tool", json={"tool_id": tool_id}, headers=auth_headers)
                if response.status_code == 200:
                    print_step("再次收集工具成功（数量+1）", True)
            else:
                print_step(f"收集工具异常: {response.status_code}", False)

        # 测试收集食物
        print_step("测试收集食物...")
        if len(FOODS_DATA) > 0:
            food_id = 1
            response = client.post("/api/v1/user/collect/food", json={"food_id": food_id}, headers=auth_headers)
            if response.status_code == 200:
                print_step("收集食物成功", True)
                # 再次收集，测试数量+1
                response = client.post("/api/v1/user/collect/food", json={"food_id": food_id}, headers=auth_headers)
                if response.status_code == 200:
                    print_step("再次收集食物成功（数量+1）", True)
            else:
                print_step(f"收集食物异常: {response.status_code}", False)

        # 测试获取用户收集的工具列表（带详情和数量）
        print_step("测试获取用户收集的工具列表（带详情）...")
        response = client.get("/api/v1/user/collect/tool/list-with-detail", headers=auth_headers)
        if response.status_code == 200:
            data = response.json()["data"]
            print_step(f"获取到用户收集的工具列表成功，共 {data['total_count']} 个", True)
            if data['items'] and len(data['items']) > 0:
                print_step(f"第一个工具的数量: {data['items'][0]['count']}", True)
        else:
            print_step(f"获取用户收集的工具列表异常: {response.status_code}", False)

        # 测试获取用户收集的食物列表（带详情和数量）
        print_step("测试获取用户收集的食物列表（带详情）...")
        response = client.get("/api/v1/user/collect/food/list-with-detail", headers=auth_headers)
        if response.status_code == 200:
            data = response.json()["data"]
            print_step(f"获取到用户收集的食物列表成功，共 {data['total_count']} 个", True)
            if data['items'] and len(data['items']) > 0:
                print_step(f"第一个食物的数量: {data['items'][0]['count']}", True)
        else:
            print_step(f"获取用户收集的食物列表异常: {response.status_code}", False)

        # 测试获取图鉴进度
        print_step("测试获取图鉴进度...")
        response = client.get("/api/v1/collection/progress", headers=auth_headers)
        if response.status_code == 200:
            data = response.json()["data"]
            print_step(f"获取到图鉴进度成功，共 {len(data['items'])} 个分类", True)
            for item in data['items']:
                print_step(f"  {item['name']}: {item['collected_count']}/{item['total_count']} ({item['progress']}%)", True)
        else:
            print_step(f"获取图鉴进度异常: {response.status_code}", False)

        # 测试用户详情（等级、宠物数量、工具、食物）
        print_step("测试用户详情...")
        response = client.get("/api/v1/user/detail", headers=auth_headers)
        if response.status_code == 200:
            user_data = response.json()["data"]
            print_step(f"当前用户等级: {user_data['level']}", True)
            print_step(f"当前宠物数量: {user_data['pet_count']}", True)
            print_step(f"当前工具数量: {user_data['tool_count']}", True)
            print_step(f"当前食物数量: {user_data['food_count']}", True)

            # 收集一些动物和植物来测试 pet_count
            print_step("收集动物和植物来测试 pet_count...")
            animal_collected = 0
            plant_collected = 0

            # 收集一些动物
            for i in range(1, min(4, len(ANIMALS_DATA) + 1)):
                response = client.post("/api/v1/user/collect/animal", json={"animal_id": i}, headers=auth_headers)
                if response.status_code == 200:
                    animal_collected += 1

            # 收集一些植物
            for i in range(1, min(3, len(PLANTS_DATA) + 1)):
                response = client.post("/api/v1/user/collect/plant", json={"plant_id": i}, headers=auth_headers)
                if response.status_code == 200:
                    plant_collected += 1

            print_step(f"收集了 {animal_collected} 只动物，{plant_collected} 株植物", True)

            # 再次检查用户详情
            response = client.get("/api/v1/user/detail", headers=auth_headers)
            if response.status_code == 200:
                user_data = response.json()["data"]
                print_step(f"收集后用户等级: {user_data['level']}", True)
                print_step(f"收集后宠物数量: {user_data['pet_count']}", True)
                print_step(f"收集后工具数量: {user_data['tool_count']}", True)
                print_step(f"收集后食物数量: {user_data['food_count']}", True)
        else:
            print_step(f"获取用户详情异常: {response.status_code}", False)

        print("\nAPI测试完成！所有主要接口正常工作。")
        return True

    except Exception as e:
        print_step(f"API测试失败: {e}", False)
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="数据库初始化脚本")
    parser.add_argument("--data", action="store_true", help="仅初始化数据（不删除数据库）")
    parser.add_argument("--test", action="store_true", help="仅测试API")
    args = parser.parse_args()

    start_time = time.time()

    print("\n" + "="*60)
    print("  Mini API 初始化脚本")
    print("="*60)

    success = True

    if args.test:
        # 仅测试API
        success = test_api()
    elif args.data:
        # 仅初始化数据
        success = init_database_data()
        if success:
            success = test_api()
    else:
        # 完整初始化
        if not delete_old_database():
            success = False
        if success:
            success = init_database_data()
        if success:
            success = test_api()

    # 总结
    elapsed = time.time() - start_time
    print_title("初始化完成")
    if success:
        print(f"  [OK] 所有操作成功完成！耗时: {elapsed:.2f}s")
        print(f"\n下一步: 运行 'python main.py' 启动服务器")
        print(f"         或访问 http://localhost:8000/docs 查看API文档")
    else:
        print(f"  [FAIL] 初始化过程中出现错误！耗时: {elapsed:.2f}s")
        sys.exit(1)


if __name__ == "__main__":
    main()
