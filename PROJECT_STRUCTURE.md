# 项目结构说明

## 目录结构

```
mini_api/
├── app/
│   ├── __init__.py
│   ├── database.py              # 数据库连接和会话管理
│   │
│   ├── models/                  # 数据模型层
│   │   ├── __init__.py
│   │   ├── category.py          # 分类模型
│   │   ├── rarity.py            # 品质模型
│   │   └── animal.py            # 动物模型
│   │
│   ├── schemas/                 # Pydantic 数据模式层
│   │   ├── __init__.py
│   │   ├── common.py            # 通用模式（分页响应等）
│   │   ├── category.py          # 分类相关模式
│   │   ├── rarity.py            # 品质相关模式
│   │   └── animal.py            # 动物相关模式
│   │
│   ├── services/                # 业务逻辑层（可选）
│   │   ├── __init__.py
│   │   ├── category_service.py  # 分类业务逻辑
│   │   ├── rarity_service.py    # 品质业务逻辑
│   │   └── animal_service.py    # 动物业务逻辑
│   │
│   └── api/                     # API 路由层
│       └── v1/
│           ├── __init__.py      # 路由聚合
│           ├── category.py      # 分类接口
│           ├── rarity.py        # 品质接口
│           └── animal.py        # 动物接口
│
├── scripts/                     # 脚本目录
│   ├── __init__.py
│   └── init_data.py             # 数据库初始化脚本
│
├── main.py                      # 应用入口
├── requirements.txt             # 依赖列表
├── reset_db.py                  # 数据库重置脚本
├── .env                         # 环境配置
└── README.md                    # 项目说明
```

## 模块职责说明

### 1. models - 数据模型层
- 定义数据库表结构
- 处理ORM映射
- 一个模型一个文件，独立管理

### 2. schemas - 数据模式层
- 定义API请求/响应的数据结构
- 处理数据验证
- 与models解耦，可独立演进

### 3. services - 业务逻辑层（可选）
- 封装核心业务逻辑
- 处理复杂的数据库操作
- 可被多个API复用
- 便于单元测试

### 4. api - 路由层
- 定义API端点
- 处理请求参数
- 调用services或直接操作models
- 返回响应数据

## 添加新模块的步骤

1. 在 `app/models/` 中创建新模型文件
2. 在 `app/schemas/` 中创建新的数据模式
3. 在 `app/services/` 中创建业务逻辑（可选）
4. 在 `app/api/v1/` 中创建API路由
5. 在 `app/api/v1/__init__.py` 中注册新路由
6. 在 `app/models/__init__.py` 和 `app/schemas/__init__.py` 中导出新模块

## 优势

✅ **清晰的职责分离** - 每层专注自己的事情
✅ **易于维护** - 修改某个模块不影响其他
✅ **便于测试** - 各层可独立测试
✅ **方便扩展** - 新增功能只需添加新文件
✅ **团队协作** - 不同人可以负责不同模块
