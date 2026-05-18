from app.schemas.common import ApiResponse, IdNameItem
from app.schemas.user import (
    UserLogin,
    UserRegister,
    UserResponse,
    UserDetail,
    UserProgress,
)
from app.schemas.animal import (
    AnimalResponse,
    AnimalDetail,
    CollectAnimalRequest,
    EditAnimalNameRequest,
    DeleteAnimalRequest,
)
from app.schemas.plant import (
    PlantResponse,
    PlantDetail,
    CollectPlantRequest,
    EditPlantNameRequest,
    DeletePlantRequest,
)
from app.schemas.tool import (
    ToolResponse,
    ToolDetail,
    CollectToolRequest,
    UseToolRequest,
    EditToolNameRequest,
    DeleteToolRequest,
    UserToolWithDetail,
    UserToolCollectionResponse,
)
from app.schemas.food import (
    FoodResponse,
    FoodDetail,
    CollectFoodRequest,
    UseFoodRequest,
    EditFoodNameRequest,
    DeleteFoodRequest,
    UserFoodWithDetail,
    UserFoodCollectionResponse,
)
from app.schemas.pet import (
    PetResponse,
    CollectPetRequest,
    EditPetNameRequest,
    DeletePetRequest,
)
from app.schemas.world import WorldResponse, WorldDetail
from app.schemas.user_collect import (
    UserAnimalResponse,
    UserPlantResponse,
    UserToolResponse,
    UserFoodResponse,
    UserPetResponse,
)
from app.schemas.collection import (
    CollectionProgressItem,
    CollectionProgressResponse,
)

__all__ = [
    "ApiResponse",
    "IdNameItem",
    "UserLogin",
    "UserRegister",
    "UserResponse",
    "UserDetail",
    "UserProgress",
    "AnimalResponse",
    "AnimalDetail",
    "CollectAnimalRequest",
    "EditAnimalNameRequest",
    "DeleteAnimalRequest",
    "PlantResponse",
    "PlantDetail",
    "CollectPlantRequest",
    "EditPlantNameRequest",
    "DeletePlantRequest",
    "ToolResponse",
    "ToolDetail",
    "CollectToolRequest",
    "UseToolRequest",
    "EditToolNameRequest",
    "DeleteToolRequest",
    "UserToolWithDetail",
    "UserToolCollectionResponse",
    "FoodResponse",
    "FoodDetail",
    "CollectFoodRequest",
    "UseFoodRequest",
    "EditFoodNameRequest",
    "DeleteFoodRequest",
    "UserFoodWithDetail",
    "UserFoodCollectionResponse",
    "PetResponse",
    "CollectPetRequest",
    "EditPetNameRequest",
    "DeletePetRequest",
    "WorldResponse",
    "WorldDetail",
    "UserAnimalResponse",
    "UserPlantResponse",
    "UserToolResponse",
    "UserFoodResponse",
    "UserPetResponse",
    "CollectionProgressItem",
    "CollectionProgressResponse",
]
