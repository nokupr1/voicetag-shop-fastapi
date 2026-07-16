from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.category import CategoryListResponse
from ..services.category import CategoryService

category_router = APIRouter(prefix="/categories")


@category_router.get("/", tags=["categories"])
async def get_all_categories(
    db: AsyncSession = Depends(get_db),
) -> CategoryListResponse:
    service = CategoryService(db)
    categories = await service.get_all()
    return CategoryListResponse(categories=categories, total=len(categories))
