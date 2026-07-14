from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.product import ProductCreate, ProductListResponse, ProductResponse
from ..services.product import ProductService

product_router = APIRouter(prefix="/products")


@product_router.post("/{product_id}", tags=["products"])
async def create_product(
    product_data: ProductCreate, db: AsyncSession = Depends(get_db)
) -> ProductResponse:
    service = ProductService(db)
    product = await service.create_product(product_data)
    return ProductResponse.model_validate(product)


@product_router.get("/", tags=["products"])
async def get_all_products(db: AsyncSession = Depends(get_db)) -> ProductListResponse:
    service = ProductService(db)
    return await service.get_all_products()


@product_router.delete("/{product_id}", tags=["products"])
async def delete_product(
    product_id: int, db: AsyncSession = Depends(get_db)
) -> ProductResponse:
    service = ProductService(db)
    product = await service.delete_product(product_id)
    return ProductResponse.model_validate(product)
