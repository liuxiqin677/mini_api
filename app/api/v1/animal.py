from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import (
    AnimalResponse, AnimalDetail, UserAnimalResponse, ApiResponse,
    CollectAnimalRequest, EditAnimalNameRequest, DeleteAnimalRequest
)
from app.services.animal_service import AnimalService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/mammals/animals/list", response_model=ApiResponse[List[AnimalResponse]])
async def get_mammals_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_animals_by_category(db, "mammal", current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.get("/birds/animals/list", response_model=ApiResponse[List[AnimalResponse]])
async def get_birds_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_animals_by_category(db, "bird", current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.get("/reptiles/animals/list", response_model=ApiResponse[List[AnimalResponse]])
async def get_reptiles_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_animals_by_category(db, "reptile", current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.get("/ocean/animals/list", response_model=ApiResponse[List[AnimalResponse]])
async def get_ocean_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_animals_by_category(db, "ocean", current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.get("/wildlife/animals/list", response_model=ApiResponse[List[AnimalResponse]])
async def get_wildlife_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_animals_by_category(db, "wildlife", current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.get("/animals/detail", response_model=ApiResponse[AnimalDetail])
async def get_animal_detail(
    animal_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animal = AnimalService.get_animal_by_id(db, animal_id, current_user.id)
    if not animal:
        raise HTTPException(status_code=404, detail="动物不存在")
    return ApiResponse(code=200, message="success", data=animal)


@router.post("/user/collect/animal", response_model=ApiResponse)
async def collect_animal(
    request: CollectAnimalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_animal = AnimalService.collect_animal(db, current_user.id, request.animal_id)
    if not user_animal:
        raise HTTPException(status_code=404, detail="动物不存在")
    return ApiResponse(code=200, message="收集成功", data=True)


@router.get("/user/collect/animal/list", response_model=ApiResponse[List[UserAnimalResponse]])
async def get_user_animals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    animals = AnimalService.get_user_animals(db, current_user.id)
    return ApiResponse(code=200, message="success", data=animals)


@router.post("/user/collect/animal/edit", response_model=ApiResponse)
async def edit_animal_name(
    request: EditAnimalNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 先查询用户的动物以获取旧名称
    from app.models import UserAnimal
    old_animal = db.query(UserAnimal).filter(
        UserAnimal.id == request.animal_id,
        UserAnimal.user_id == current_user.id
    ).first()

    if not old_animal:
        raise HTTPException(status_code=404, detail="记录不存在")

    old_name = old_animal.name

    user_animal = AnimalService.edit_animal_name(db, request.animal_id, current_user.id, request.name, old_name)
    if not user_animal:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="编辑成功", data=True)


@router.delete("/user/collect/animal/delete", response_model=ApiResponse)
async def delete_animal(
    request: DeleteAnimalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = AnimalService.delete_animal(db, request.animal_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="删除成功", data=True)
