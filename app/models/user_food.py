from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class UserFood(Base):
    __tablename__ = "user_foods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    food_id = Column(Integer, nullable=False, index=True)
    name = Column(String(50), nullable=False, comment="食物名称（可自定义）")
    description = Column(String(200), nullable=True, comment="描述")
    rarity = Column(String(20), nullable=False, comment="稀有度")
    count = Column(Integer, nullable=False, default=1, comment="收集数量")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="user_foods")
