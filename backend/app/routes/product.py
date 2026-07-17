from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.product import ProductCreate, ProductListResponse, ProductResponse
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
async def create(
    product_data: ProductCreate, db: AsyncSession = Depends(get_db)
) -> ProductResponse:
    service = ProductService(db)
    product = await service.create_product(product_data)
    return ProductResponse.model_validate(product)
