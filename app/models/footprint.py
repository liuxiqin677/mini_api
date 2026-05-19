from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Footprint(Base):
    __tablename__ = "footprints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # 操作类型: collect, edit, delete, feed, pet, water, fertilize
    action_type = Column(String(50), nullable=False, comment="操作类型")

    # 目标类型: animal, plant
    target_type = Column(String(50), nullable=False, comment="目标类型")
    target_id = Column(Integer, nullable=False, comment="目标ID")
    target_name = Column(String(200), nullable=False, comment="目标名称")

    # 详细描述
    detail = Column(Text, nullable=True, comment="详细描述")

    # 变化值（如 love 增长了多少）
    change_value = Column(Integer, nullable=True, comment="变化值")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", back_populates="footprints")
