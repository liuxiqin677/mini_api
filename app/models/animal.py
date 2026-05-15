from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="动物名称")
    emoji = Column(String(10), nullable=False, comment="emoji")
    description = Column(String(200), nullable=False, comment="描述")
    rarity = Column(String(20), nullable=False, comment="稀有度: common, rare, epic, legendary")
    category = Column(String(50), nullable=False, comment="分类: mammal, bird, reptile, ocean, wildlife")
    favorite_food_ids = Column(JSON, nullable=True, comment="喜欢的食物ID列表")
    tool_ids = Column(JSON, nullable=True, comment="增加捕捉率的工具ID列表")
    world_ids = Column(JSON, nullable=True, comment="出现的世界ID列表")
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)

    # 关系
    user_animals = relationship("UserAnimal", back_populates="animal", cascade="all, delete-orphan")
