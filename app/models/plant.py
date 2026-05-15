from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="植物名称")
    emoji = Column(String(10), nullable=False, comment="emoji")
    description = Column(String(200), nullable=False, comment="描述")
    rarity = Column(String(20), nullable=False, comment="稀有度: common, rare, epic, legendary")
    favorite_food_ids = Column(JSON, nullable=True, comment="喜欢的肥料ID列表")
    tool_ids = Column(JSON, nullable=True, comment="增加收集率的工具ID列表")
    world_ids = Column(JSON, nullable=True, comment="出现的世界ID列表")
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
