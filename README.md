# Mini API

奇域小程序后端项目。基于 Python + FastAPI + SQLite 的收集类游戏后端项目。

## 目录结构

```
mini_api/
├── app/
│   ├── __init__.py
│   ├── database.py              # 数据库连接和会话管理
│   │
│   ├── api/                     # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py              # 依赖项（获取当前用户等）
│   │   └── v1/
│   │       ├── __init__.py      # v1 路由聚合
│   │       ├── animal.py        # 动物相关接口
│   │       ├── plant.py         # 植物相关接口
│   │       ├── tool.py          # 工具相关接口
│   │       ├── food.py          # 食物相关接口
│   │       ├── pet.py           # 宠物相关接口
│   │       ├── world.py         # 世界相关接口
│   │       ├── auth.py          # 认证相关接口
│   │       ├── user.py          # 用户相关接口
│   │       └── collection.py    # 图鉴进度接口
│   │
│   ├── models/                  # 数据模型层（SQLAlchemy ORM）
│   │   ├── __init__.py
│   │   ├── user.py              # 用户模型
│   │   ├── animal.py            # 动物模型
│   │   ├── plant.py             # 植物模型
│   │   ├── tool.py              # 工具模型
│   │   ├── food.py              # 食物模型
│   │   ├── pet.py               # 宠物模型
│   │   ├── world.py             # 世界模型
│   │   ├── user_animal.py       # 用户-动物关联模型
│   │   ├── user_plant.py        # 用户-植物关联模型
│   │   ├── user_tool.py         # 用户-工具关联模型
│   │   ├── user_food.py         # 用户-食物关联模型
│   │   └── user_pet.py          # 用户-宠物关联模型
│   │
│   ├── schemas/                 # Pydantic 数据模式层
│   │   ├── __init__.py
│   │   ├── common.py            # 通用模式（API 响应包装等）
│   │   ├── user.py              # 用户相关模式
│   │   ├── animal.py            # 动物相关模式
│   │   ├── plant.py             # 植物相关模式
│   │   ├── tool.py              # 工具相关模式
│   │   ├── food.py              # 食物相关模式
│   │   ├── pet.py               # 宠物相关模式
│   │   ├── world.py             # 世界相关模式
│   │   ├── user_collect.py      # 用户收集项相关模式
│   │   └── collection.py        # 图鉴进度相关模式
│   │
│   ├── services/                # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py      # 用户业务逻辑
│   │   ├── animal_service.py    # 动物业务逻辑
│   │   ├── plant_service.py     # 植物业务逻辑
│   │   ├── tool_service.py      # 工具业务逻辑
│   │   ├── food_service.py      # 食物业务逻辑
│   │   ├── pet_service.py       # 宠物业务逻辑
│   │   ├── world_service.py     # 世界业务逻辑
│   │   ├── level_service.py     # 等级计算业务逻辑
│   │   └── collection_service.py # 图鉴进度业务逻辑
│   │
│   └── core/                    # 核心功能模块
│       ├── __init__.py
│       └── security.py          # 安全相关（密码哈希、JWT等）
│
├── scripts/                     # 脚本目录
│   └── __init__.py
│
├── main.py                      # FastAPI 应用入口
├── init.py                      # 数据库初始化（删除旧库、创建表、填充数据、测试接口）
├── requirements.txt             # Python 依赖列表
├── .env                         # 环境变量配置
├── .env.example                 # 环境变量示例
├── API_DOCS.md                  # API 接口详细文档
├── DATA.md                      # 初始化数据说明文档
├── PROJECT_STRUCTURE.md         # 项目结构详细说明
└── README.md                    # 本文件
```

## 目录职责说明

### 1. `/app/models/` - 数据模型层
- 定义数据库表结构
- 使用 SQLAlchemy ORM 进行对象关系映射
- 一个模型对应一个数据库表
- 定义表之间的关系（外键关联等）

### 2. `/app/schemas/` - 数据模式层
- 定义 API 请求/响应的数据结构
- 使用 Pydantic 进行数据验证
- 与 models 解耦，可独立演进
- 包含基础响应（Response）、详情（Detail）、请求（Request）等模式

### 3. `/app/services/` - 业务逻辑层
- 封装核心业务逻辑
- 处理复杂的数据库操作
- 可被多个 API 复用
- 便于单元测试
- 从 models 读取数据，返回 schemas 格式

### 4. `/app/api/` - 路由层
- 定义 API 端点
- 处理请求参数验证
- 调用 services 处理业务逻辑
- 返回标准化的响应数据
- 版本化管理（v1/）

### 5. `/app/core/` - 核心功能
- 安全相关功能
- 密码哈希验证
- JWT token 生成和验证

### 6. `/scripts/` - 脚本目录
- 存放各种工具脚本
- 数据库迁移脚本等

## 数据库表结构与关系

### 表概览

| 表名 | 说明 | 主要功能 |
|------|------|----------|
| users | 用户表 | 存储用户账号信息 |
| animals | 动物表 | 存储所有动物基础数据 |
| plants | 植物表 | 存储所有植物基础数据 |
| tools | 工具表 | 存储所有工具基础数据 |
| foods | 食物表 | 存储所有食物基础数据 |
| pets | 宠物表 | 存储所有宠物基础数据 |
| worlds | 世界表 | 存储世界/地图信息 |
| user_animals | 用户-动物关联表 | 记录用户收集的动物 |
| user_plants | 用户-植物关联表 | 记录用户收集的植物 |
| user_tools | 用户-工具关联表 | 记录用户收集的工具 |
| user_foods | 用户-食物关联表 | 记录用户收集的食物 |
| user_pets | 用户-宠物关联表 | 记录用户收集的宠物 |

### ER 图 - 表关系

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             USER 相关表                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐       ┌──────────────────┐       ┌─────────────────┐  │
│  │   users         │       │  user_animals    │       │   animals       │  │
│  ├─────────────────┤       ├──────────────────┤       ├─────────────────┤  │
│  │ id (PK)         │◄──────│ id (PK)          │──────►│ id (PK)         │  │
│  │ username        │ 1   N │ user_id (FK)     │ N   1 │ name            │  │
│  │ hashed_password │       │ animal_id (FK)   │       │ emoji           │  │
│  │ level           │       │ name             │       │ description     │  │
│  │ created_at      │       │ description      │       │ rarity          │  │
│  │ updated_at      │       │ rarity           │       │ category        │  │
│  └─────────────────┘       │ created_at       │       │ favorite_food_ids│ │
│         │                   │ updated_at       │       │ tool_ids        │  │
│         │                   └──────────────────┘       │ world_ids       │  │
│         │                                              └─────────────────┘  │
│         │                                              ┌─────────────────┐  │
│         │                                              │   plants        │  │
│         │                                              ├─────────────────┤  │
│         │                                              │ id (PK)         │  │
│         │                   ┌──────────────────┐      │ name            │  │
│         │                   │  user_plants     │      │ emoji           │  │
│         │                   ├──────────────────┤      │ description     │  │
│         │                   │ id (PK)          │      │ rarity          │  │
│         │                   │ user_id (FK)     │      │ favorite_food_ids││
│         ├──────────────────►│ plant_id         │      │ tool_ids        │  │
│         │   1             N │ name             │      │ world_ids       │  │
│         │                   │ description      │      └─────────────────┘  │
│         │                   │ rarity           │                             │
│         │                   │ created_at       │      ┌─────────────────┐  │
│         │                   │ updated_at       │      │     tools       │  │
│         │                   └──────────────────┘      ├─────────────────┤  │
│         │                                              │ id (PK)         │  │
│         │                                              │ name            │  │
│         │                   ┌──────────────────┐      │ emoji           │  │
│         │                   │  user_tools      │      │ description     │  │
│         │                   ├──────────────────┤      │ rarity          │  │
│         │                   │ id (PK)          │      │ world_ids       │  │
│         ├──────────────────►│ user_id (FK)     │      │ target_ids      │  │
│         │   1             N │ tool_id          │      └─────────────────┘  │
│         │                   │ name             │                             │
│         │                   │ description      │      ┌─────────────────┐  │
│         │                   │ rarity           │      │     foods       │  │
│         │                   │ count            │      ├─────────────────┤  │
│         │                   │ created_at       │      │ id (PK)         │  │
│         │                   │ updated_at       │      │ name            │  │
│         │                   └──────────────────┘      │ emoji           │  │
│         │                                              │ description     │  │
│         │                                              │ rarity          │  │
│         │                   ┌──────────────────┐      │ world_ids       │  │
│         │                   │  user_foods      │      │ target_ids      │  │
│         │                   ├──────────────────┤      └─────────────────┘  │
│         │                   │ id (PK)          │                             │
│         ├──────────────────►│ user_id (FK)     │      ┌─────────────────┐  │
│         │   1             N │ food_id          │      │     pets        │  │
│         │                   │ name             │      ├─────────────────┤  │
│         │                   │ description      │      │ id (PK)         │  │
│         │                   │ rarity           │      │ name            │  │
│         │                   │ count            │      │ emoji           │  │
│         │                   │ created_at       │      │ description     │  │
│         │                   │ updated_at       │      │ rarity          │  │
│         │                   └──────────────────┘      │ world_ids       │  │
│         │                                              └─────────────────┘  │
│         │                                                                   │
│         │                   ┌──────────────────┐                             │
│         │                   │  user_pets       │                             │
│         │                   ├──────────────────┤                             │
│         │                   │ id (PK)          │                             │
│         └──────────────────►│ user_id (FK)     │                             │
│             1             N │ pet_id           │                             │
│                             │ name             │                             │
│                             │ description      │                             │
│                             │ rarity           │                             │
│                             │ created_at       │                             │
│                             │ updated_at       │                             │
│                             └──────────────────┘                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              WORLD 表                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                              worlds                                     │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ id (PK)                                                                 │  │
│  │ name                                                                   │  │
│  │ emoji                                                                  │  │
│  │ description                                                            │  │
│  │ bg_color                                                               │  │
│  │ gradient                                                               │  │
│  │ animal_ids (JSON)  ──────────┐  (引用 animals 表 id 列表)              │  │
│  │ plant_ids (JSON)   ──────────┼─┐ (引用 plants 表 id 列表)               │  │
│  │ tool_ids (JSON)    ──────────┼─┼─┐ (引用 tools 表 id 列表)              │  │
│  │ food_ids (JSON)    ──────────┼─┼─┼─┐ (引用 foods 表 id 列表)             │  │
│  │ created_at                  │ │ │ │                                     │  │
│  │ updated_at                  │ │ │ │                                     │  │
│  └─────────────────────────────┼─┼─┼─┘                                     │  │
│                                │ │ │                                       │  │
│  ┌─────────────────┐◄──────────┘ │ │  ┌─────────────────┐                  │  │
│  │   animals       │             │ │  │     plants      │                  │  │
│  └─────────────────┘◄────────────┘ │  └─────────────────┘                  │  │
│                                    │                                       │  │
│  ┌─────────────────┐◄──────────────┘  ┌─────────────────┐                  │  │
│  │     tools       │                   │     foods       │                  │  │
│  └─────────────────┘                   └─────────────────┘                  │  │
│                                                                              │  │
│  (通过 world_ids 反向关联：animal.world_ids 包含 world.id)                   │  │
│                                                                              │  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 表关系详解

#### 1. 用户与收集项的关系（一对多）
- **User → UserAnimal**: 一个用户可以收集多个动物
- **User → UserPlant**: 一个用户可以收集多个植物
- **User → UserTool**: 一个用户可以收集多个工具（支持数量累计）
- **User → UserFood**: 一个用户可以收集多个食物（支持数量累计）
- **User → UserPet**: 一个用户可以收集多个宠物

#### 2. 动物/植物与工具/食物的关系（多对多，通过 JSON 数组）
- **Animal.favorite_food_ids**: JSON 数组，存储该动物喜欢的食物 ID 列表
- **Animal.tool_ids**: JSON 数组，存储可以增加捕获该动物概率的工具 ID 列表
- **Plant.favorite_food_ids**: JSON 数组，存储该植物喜欢的肥料 ID 列表
- **Plant.tool_ids**: JSON 数组，存储可以增加收集该植物概率的工具 ID 列表

#### 3. 工具/食物与目标的关系（多对多，通过 JSON 数组）
- **Tool.target_ids**: JSON 数组，存储该工具适用的动物/植物 ID 列表
- **Food.target_ids**: JSON 数组，存储该食物适用的动物/植物 ID 列表

#### 4. 世界与生物的关系（多对多，通过 JSON 数组）
- **World.animal_ids**: JSON 数组，存储该世界中出现的动物 ID 列表
- **World.plant_ids**: JSON 数组，存储该世界中出现的植物 ID 列表
- **World.tool_ids**: JSON 数组，存储该世界中出现的工具 ID 列表
- **World.food_ids**: JSON 数组，存储该世界中出现的食物 ID 列表
- **Animal.world_ids**: JSON 数组，反向关联，存储该动物出现的世界 ID 列表
- **Plant.world_ids**: JSON 数组，反向关联，存储该植物出现的世界 ID 列表
- **Tool.world_ids**: JSON 数组，反向关联，存储该工具出现的世界 ID 列表
- **Food.world_ids**: JSON 数组，反向关联，存储该食物出现的世界 ID 列表
- **Pet.world_ids**: JSON 数组，反向关联，存储该宠物出现的世界 ID 列表

### 字段说明

#### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| username | String(20) | 用户名，唯一 |
| hashed_password | String | 哈希后的密码 |
| level | Integer | 用户等级，默认 1 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 动物表 (animals)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 动物名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度：common/rare/epic/legendary |
| category | String(50) | 分类：mammal/bird/reptile/ocean/wildlife |
| favorite_food_ids | JSON | 喜欢的食物 ID 列表 |
| tool_ids | JSON | 增加捕获率的工具 ID 列表 |
| world_ids | JSON | 出现的世界 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 植物表 (plants)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 植物名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度：common/rare/epic/legendary |
| favorite_food_ids | JSON | 喜欢的肥料 ID 列表 |
| tool_ids | JSON | 增加收集率的工具 ID 列表 |
| world_ids | JSON | 出现的世界 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 工具表 (tools)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 工具名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度：common/rare/epic/legendary |
| world_ids | JSON | 出现的世界 ID 列表 |
| target_ids | JSON | 适用的动物/植物 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 食物表 (foods)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 食物名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度：common/rare/epic/legendary |
| world_ids | JSON | 出现的世界 ID 列表 |
| target_ids | JSON | 适用的动物/植物 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 宠物表 (pets)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 宠物名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度：common/rare/epic/legendary |
| world_ids | JSON | 出现的世界 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 世界表 (worlds)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(50) | 世界名称 |
| emoji | String(10) | 表情符号 |
| description | String(200) | 描述 |
| bg_color | String(20) | 背景颜色 |
| gradient | String(50) | 渐变色 |
| animal_ids | JSON | 出现的动物 ID 列表 |
| plant_ids | JSON | 出现的植物 ID 列表 |
| tool_ids | JSON | 出现的工具 ID 列表 |
| food_ids | JSON | 出现的食物 ID 列表 |
| created_at | String | 创建时间 |
| updated_at | String | 更新时间 |

#### 用户-动物关联表 (user_animals)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| user_id | Integer | 用户 ID，外键关联 users.id |
| animal_id | Integer | 动物 ID，外键关联 animals.id |
| name | String(50) | 动物名称（用户可自定义） |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 用户-植物关联表 (user_plants)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| user_id | Integer | 用户 ID，外键关联 users.id |
| plant_id | Integer | 植物 ID |
| name | String(50) | 植物名称（用户可自定义） |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 用户-工具关联表 (user_tools)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| user_id | Integer | 用户 ID，外键关联 users.id |
| tool_id | Integer | 工具 ID |
| name | String(50) | 工具名称（用户可自定义） |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度 |
| count | Integer | 收集数量，默认 1 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 用户-食物关联表 (user_foods)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| user_id | Integer | 用户 ID，外键关联 users.id |
| food_id | Integer | 食物 ID |
| name | String(50) | 食物名称（用户可自定义） |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度 |
| count | Integer | 收集数量，默认 1 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 用户-宠物关联表 (user_pets)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| user_id | Integer | 用户 ID，外键关联 users.id |
| pet_id | Integer | 宠物 ID |
| name | String(50) | 宠物名称（用户可自定义） |
| description | String(200) | 描述 |
| rarity | String(20) | 稀有度 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 快速开始

### 1. 安装依赖

```bash
cd mini_api
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init.py
```

这个脚本会：
- 删除旧的数据库文件（如果存在）
- 重新创建所有数据表
- 填充初始数据（世界、动物、植物、工具、食物、宠物）
- 自动测试所有 API 接口

参数选项：
```bash
python init.py --data     # 仅初始化数据（保留数据库结构）
python init.py --test     # 仅测试 API 接口
```

### 3. 启动服务

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload
```

## API 文档

启动服务后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

详细的 API 接口文档请参考 [API_DOCS.md](./API_DOCS.md)

## 初始化数据说明

初始化数据包括：
- 6 个世界
- 19 种动物（分为哺乳动物、鸟类、爬行动物、海洋生物、野生动物）
- 7 种植物
- 6 种工具
- 8 种食物
- 5 种宠物

详细数据说明请参考 [DATA.md](./DATA.md)

## 项目结构详细说明

关于项目结构的更详细说明请参考 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 技术栈

- **FastAPI**: 现代、快速（高性能）的 Web 框架
- **SQLAlchemy**: Python SQL 工具和 ORM
- **Pydantic**: 数据验证和设置管理
- **SQLite**: 轻量级数据库
- **Python-Jose**: JWT token 生成和验证
- **Passlib**: 密码哈希

## 开发指南

### 添加新模块的步骤

1. 在 `app/models/` 中创建新模型文件
2. 在 `app/schemas/` 中创建新的数据模式
3. 在 `app/services/` 中创建业务逻辑
4. 在 `app/api/v1/` 中创建 API 路由
5. 在 `app/api/v1/__init__.py` 中注册新路由
6. 在 `app/models/__init__.py` 和 `app/schemas/__init__.py` 中导出新模块
7. 在 `init.py` 中添加初始化数据（如需要）

## 许可证

MIT License
