# Mini API

基于 FastAPI + SQLite 的后端项目，提供动物数据 API。

## 快速开始

### 1. 安装依赖

```bash
cd mini_api
pip install -r requirements.txt
```

### 2. 初始化数据

```bash
python scripts/init_data.py
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

## API 接口

### GET /api/v1/animal/list

获取动物列表

返回示例：

```json
{
  "data": [
    {
      "id": 1,
      "name": "小橘猫",
      "emoji": "🐱",
      "category": "cat",
      "rarity": "common",
      "isFind": false
    }
  ],
  "total": 10
}
```

## 项目结构

```
mini_api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── animals.py
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── scripts/
│   ├── __init__.py
│   └── init_data.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```
