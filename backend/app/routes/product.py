from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.product import ProductListResponse, ProductResponse
from ..services.product import ProductService

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.get("/")
async def get_all_products(db: AsyncSession = Depends(get_db)) -> ProductListResponse:
    service = ProductService(db)
    return await service.get_all_products()


@product_router.get(path="/{product_id}")
async def get_product(
    product_id: int, db: AsyncSession = Depends(get_db)
) -> ProductResponse:
    service = ProductService(db)
    return await service.get_product(product_id)


@product_router.post(path="/category/{category_id}")
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_db)
) -> ProductListResponse:
    service = ProductService(db)
    return await service.get_products_by_category(category_id)
