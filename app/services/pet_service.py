from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Pet, UserPet
from app.schemas import PetResponse, UserPetResponse


class PetService:
    @staticmethod
    def get_all_pets(db: Session, user_id: int) -> List[PetResponse]:
        pets = db.query(Pet).all()
        user_collected_ids = {up.pet_id for up in db.query(UserPet.pet_id).filter(UserPet.user_id == user_id).all()}

        result = []
        for pet in pets:
            result.append(PetResponse(
                id=pet.id,
                name=pet.name,
                emoji=pet.emoji,
                description=pet.description,
                rarity=pet.rarity,
                is_collected=pet.id in user_collected_ids,
                world_ids=pet.world_ids,
                created_at=pet.created_at,
                updated_at=pet.updated_at
            ))
        return result

    @staticmethod
    def collect_pet(db: Session, user_id: int, pet_id: int) -> Optional[UserPet]:
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet:
            return None

        user_pet = UserPet(
            user_id=user_id,
            pet_id=pet_id,
            name=pet.name,
            description=pet.description,
            rarity=pet.rarity
        )
        db.add(user_pet)
        db.commit()
        db.refresh(user_pet)
        return user_pet

    @staticmethod
    def get_user_pets(db: Session, user_id: int) -> List[UserPetResponse]:
        user_pets = db.query(UserPet).filter(UserPet.user_id == user_id).all()
        result = []
        for up in user_pets:
            result.append(UserPetResponse(
                id=up.id,
                user_id=up.user_id,
                pet_id=up.pet_id,
                name=up.name,
                description=up.description,
                rarity=up.rarity,
                created_at=up.created_at,
                updated_at=up.updated_at
            ))
        return result

    @staticmethod
    def edit_pet_name(db: Session, user_pet_id: int, user_id: int, name: str) -> Optional[UserPet]:
        user_pet = db.query(UserPet).filter(
            UserPet.id == user_pet_id,
            UserPet.user_id == user_id
        ).first()
        if not user_pet:
            return None

        user_pet.name = name
        db.commit()
        db.refresh(user_pet)
        return user_pet

    @staticmethod
    def delete_pet(db: Session, user_pet_id: int, user_id: int) -> bool:
        user_pet = db.query(UserPet).filter(
            UserPet.id == user_pet_id,
            UserPet.user_id == user_id
        ).first()
        if not user_pet:
            return False

        db.delete(user_pet)
        db.commit()
        return True
