from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
<<<<<<< HEAD
from ..schemas.category import CategoryListResponse, CategoryResponse
from ..services.category import CategoryService

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("/")
=======
from ..schemas.category import CategoryListResponse
from ..services.category import CategoryService

category_router = APIRouter(prefix="/categories")


@category_router.get("/", tags=["categories"])
>>>>>>> a1ea5748c597144fda260245ab6181892ce99813
async def get_all_categories(
    db: AsyncSession = Depends(get_db),
) -> CategoryListResponse:
    service = CategoryService(db)
    categories = await service.get_all()
    return CategoryListResponse(categories=categories, total=len(categories))
<<<<<<< HEAD


@category_router.get(path="/{category_id}")
async def get_category(
    category_id: int, db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    service = CategoryService(db)
    category = await service.get_by_id(category_id)
    return CategoryResponse.model_validate(category)
=======
>>>>>>> a1ea5748c597144fda260245ab6181892ce99813
