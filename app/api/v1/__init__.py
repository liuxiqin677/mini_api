from fastapi import APIRouter
from app.api.v1 import user, auth, animal, plant, tool, food, pet, world, collection

router = APIRouter()

router.include_router(user.router, prefix="/user", tags=["用户"])
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(animal.router, prefix="", tags=["动物"])
router.include_router(plant.router, prefix="", tags=["植物"])
router.include_router(tool.router, prefix="", tags=["工具"])
router.include_router(food.router, prefix="", tags=["食物"])
router.include_router(pet.router, prefix="", tags=["宠物"])
router.include_router(world.router, prefix="", tags=["世界"])
router.include_router(collection.router, prefix="", tags=["图鉴"])
