# Mini API 文档

## 概述

这是一个用于收集动物、植物、工具、食物和宠物的后端API。所有API都需要认证（除了登录）。

## 认证

### 用户登录

**请求:**
```
POST /api/v1/user/login
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "用户名",
    "token": "JWT token"
  }
}
```

**注意:** 如果用户不存在，会自动创建新用户。

### 使用认证

后续所有请求都需要在请求头中携带token：
```
Authorization: Bearer <token>
```

如果token无效或过期，API会返回403状态码。

---

## 用户接口

### 获取用户详情

```
GET /api/v1/user/detail
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "用户名",
    "level": 1,
    "food_count": 0,
    "tool_count": 0,
    "pet_count": 0,
    "created_at": "时间",
    "updated_at": "时间"
  }
}
```

### 获取收集进度

```
GET /api/v1/user/collect/progress
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": 1,
    "collected_count": 0,
    "total_count": 50
  }
}
```

---

## 动物接口

### 获取哺乳动物列表

```
GET /api/v1/mammals/animals/list
```

### 获取鸟类列表

```
GET /api/v1/birds/animals/list
```

### 获取爬行动物列表

```
GET /api/v1/reptiles/animals/list
```

### 获取海洋生物列表

```
GET /api/v1/ocean/animals/list
```

### 获取野生动物列表

```
GET /api/v1/wildlife/animals/list
```

### 获取动物详情

```
GET /api/v1/animals/detail?animal_id=1
```

### 收集动物

```
POST /api/v1/user/collect/animal
Content-Type: application/json

{
  "animal_id": 1
}
```

### 获取用户收集的动物列表

```
GET /api/v1/user/collect/animal/list
```

### 编辑动物名称

```
POST /api/v1/user/collect/animal/edit
Content-Type: application/json

{
  "animal_id": 1,
  "name": "新名字"
}
```

### 删除动物

```
DELETE /api/v1/user/collect/animal/delete
Content-Type: application/json

{
  "animal_id": 1
}
```

---

## 植物接口

### 获取植物列表

```
GET /api/v1/plants/animals/list
```

### 获取植物详情

```
GET /api/v1/plants/detail?plant_id=1
```

### 收集植物

```
POST /api/v1/user/collect/plant
Content-Type: application/json

{
  "plant_id": 1
}
```

### 获取用户收集的植物列表

```
GET /api/v1/user/collect/plant/list
```

### 编辑植物名称

```
POST /api/v1/user/collect/plant/edit
Content-Type: application/json

{
  "plant_id": 1,
  "name": "新名字"
}
```

### 删除植物

```
DELETE /api/v1/user/collect/plant/delete
Content-Type: application/json

{
  "plant_id": 1
}
```

---

## 工具接口

### 获取工具列表

```
GET /api/v1/tools/list
```

### 获取工具详情

```
GET /api/v1/tools/detail?tool_id=1
```

### 收集工具

```
POST /api/v1/user/collect/tool
Content-Type: application/json

{
  "tool_id": 1
}
```

### 获取用户收集的工具列表

```
GET /api/v1/user/collect/tool/list
```

### 编辑工具名称

```
POST /api/v1/user/collect/tool/edit
Content-Type: application/json

{
  "tool_id": 1,
  "name": "新名字"
}
```

### 删除工具

```
DELETE /api/v1/user/collect/tool/delete
Content-Type: application/json

{
  "tool_id": 1
}
```

---

## 食物接口

### 获取食物列表

```
GET /api/v1/foods/list
```

### 获取食物详情

```
GET /api/v1/foods/detail?food_id=1
```

### 收集食物

```
POST /api/v1/user/collect/food
Content-Type: application/json

{
  "food_id": 1
}
```

### 获取用户收集的食物列表

```
GET /api/v1/user/collect/food/list
```

### 编辑食物名称

```
POST /api/v1/user/collect/food/edit
Content-Type: application/json

{
  "food_id": 1,
  "name": "新名字"
}
```

### 删除食物

```
DELETE /api/v1/user/collect/food/delete
Content-Type: application/json

{
  "food_id": 1
}
```

---

## 宠物接口

### 收集宠物

```
POST /api/v1/user/collect/pet
Content-Type: application/json

{
  "pet_id": 1
}
```

### 获取用户收集的宠物列表

```
GET /api/v1/user/collect/pet/list
```

### 编辑宠物名称

```
POST /api/v1/user/collect/pet/edit
Content-Type: application/json

{
  "pet_id": 1,
  "name": "新名字"
}
```

### 删除宠物

```
DELETE /api/v1/user/collect/pet/delete
Content-Type: application/json

{
  "pet_id": 1
}
```

---

## 世界接口

### 获取世界列表

```
GET /api/v1/world/list
```

### 获取世界详情

```
GET /api/v1/world/detail?world_id=1
```

---

## 数据结构

### 动物/植物/工具/食物/宠物

```json
{
  "id": 1,
  "name": "名称",
  "emoji": "🦁",
  "description": "描述",
  "rarity": "common|rare|epic|legendary",
  "is_collected": false,
  "world_ids": [1, 2, 3],
  "created_at": null,
  "updated_at": null
}
```

动物额外有 `category` 字段。

### 世界

```json
{
  "id": 1,
  "name": "草原",
  "emoji": "🦁",
  "description": "温血脊椎动物",
  "bg_color": "#FFF5E6",
  "gradient": "linear-gradient(...)",
  "animal_ids": [1, 2, 3],
  "plant_ids": [1],
  "tool_ids": [1],
  "food_ids": [1, 2],
  "created_at": null,
  "updated_at": null
}
```

### 用户收集的项目

```json
{
  "id": 1,
  "user_id": 1,
  "animal_id": 1,
  "name": "名称",
  "description": "描述",
  "rarity": "common",
  "created_at": "时间",
  "updated_at": "时间"
}
```

---

## 初始化数据库

运行以下命令初始化数据库：

```bash
python reset_and_init.py
```

或者：

```bash
python -m scripts.init_data
```

---

## 启动服务器

```bash
python main.py
```

或者使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问API文档：http://localhost:8000/docs
