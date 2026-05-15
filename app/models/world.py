from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="世界名称")
    emoji = Column(String(10), nullable=False, comment="emoji")
    description = Column(String(200), nullable=False, comment="描述")
    bg_color = Column(String(20), nullable=True, comment="背景颜色")
    gradient = Column(String(50), nullable=True, comment="渐变色")
    animal_ids = Column(JSON, nullable=True, comment="出现的动物ID列表")
    plant_ids = Column(JSON, nullable=True, comment="出现的植物ID列表")
    tool_ids = Column(JSON, nullable=True, comment="出现的工具ID列表")
    food_ids = Column(JSON, nullable=True, comment="出现的食物ID列表")
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
