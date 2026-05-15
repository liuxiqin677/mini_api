from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Animal, UserAnimal
from app.schemas import AnimalResponse, AnimalDetail, UserAnimalResponse


class AnimalService:
    @staticmethod
    def get_animals_by_category(db: Session, category: str, user_id: int) -> List[AnimalResponse]:
        animals = db.query(Animal).filter(Animal.category == category).all()
        user_collected_ids = {ua.animal_id for ua in db.query(UserAnimal.animal_id).filter(UserAnimal.user_id == user_id).all()}

        result = []
        for animal in animals:
            result.append(AnimalResponse(
                id=animal.id,
                name=animal.name,
                emoji=animal.emoji,
                description=animal.description,
                rarity=animal.rarity,
                category=animal.category,
                is_collected=animal.id in user_collected_ids,
                favorite_food_ids=animal.favorite_food_ids,
                tool_ids=animal.tool_ids,
                world_ids=animal.world_ids,
                created_at=animal.created_at,
                updated_at=animal.updated_at
            ))
        return result

    @staticmethod
    def get_animal_by_id(db: Session, animal_id: int, user_id: int) -> Optional[AnimalDetail]:
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if not animal:
            return None

        user_collected = db.query(UserAnimal).filter(
            UserAnimal.user_id == user_id,
            UserAnimal.animal_id == animal_id
        ).first()

        return AnimalDetail(
            id=animal.id,
            name=animal.name,
            emoji=animal.emoji,
            description=animal.description,
            rarity=animal.rarity,
            category=animal.category,
            is_collected=user_collected is not None,
            favorite_food_ids=animal.favorite_food_ids,
            tool_ids=animal.tool_ids,
            world_ids=animal.world_ids,
            created_at=animal.created_at,
            updated_at=animal.updated_at
        )

    @staticmethod
    def collect_animal(db: Session, user_id: int, animal_id: int) -> Optional[UserAnimal]:
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if not animal:
            return None

        user_animal = UserAnimal(
            user_id=user_id,
            animal_id=animal_id,
            name=animal.name,
            description=animal.description,
            rarity=animal.rarity
        )
        db.add(user_animal)
        db.commit()
        db.refresh(user_animal)
        return user_animal

    @staticmethod
    def get_user_animals(db: Session, user_id: int) -> List[UserAnimalResponse]:
        user_animals = db.query(UserAnimal).filter(UserAnimal.user_id == user_id).all()
        result = []
        for ua in user_animals:
            result.append(UserAnimalResponse(
                id=ua.id,
                user_id=ua.user_id,
                animal_id=ua.animal_id,
                name=ua.name,
                description=ua.description,
                rarity=ua.rarity,
                created_at=ua.created_at,
                updated_at=ua.updated_at
            ))
        return result

    @staticmethod
    def edit_animal_name(db: Session, user_animal_id: int, user_id: int, name: str) -> Optional[UserAnimal]:
        user_animal = db.query(UserAnimal).filter(
            UserAnimal.id == user_animal_id,
            UserAnimal.user_id == user_id
        ).first()
        if not user_animal:
            return None

        user_animal.name = name
        db.commit()
        db.refresh(user_animal)
        return user_animal

    @staticmethod
    def delete_animal(db: Session, user_animal_id: int, user_id: int) -> bool:
        user_animal = db.query(UserAnimal).filter(
            UserAnimal.id == user_animal_id,
            UserAnimal.user_id == user_id
        ).first()
        if not user_animal:
            return False

        db.delete(user_animal)
        db.commit()
        return True
