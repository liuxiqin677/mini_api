from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user_animals = relationship("UserAnimal", back_populates="user", cascade="all, delete-orphan")
    user_plants = relationship("UserPlant", back_populates="user", cascade="all, delete-orphan")
    user_tools = relationship("UserTool", back_populates="user", cascade="all, delete-orphan")
    user_foods = relationship("UserFood", back_populates="user", cascade="all, delete-orphan")
    user_pets = relationship("UserPet", back_populates="user", cascade="all, delete-orphan")
    footprints = relationship("Footprint", back_populates="user", cascade="all, delete-orphan")
