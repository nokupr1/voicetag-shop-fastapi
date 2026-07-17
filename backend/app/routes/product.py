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
<<<<<<< HEAD
    return await service.get_product(product_id)


@product_router.post(path="/category/{category_id}")
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_db)
) -> ProductListResponse:
    service = ProductService(db)
    return await service.get_products_by_category(category_id)
=======
    product = await service.delete_product(product_id)
    return ProductResponse.model_validate(product)


@product_router.patch("/", tags=["products"])
async def update_product(
    product_id: int, product_data: ProductCreate, db: AsyncSession = Depends(get_db)
) -> ProductResponse:
    service = ProductService(db)
    product = await service.update_product(product_id, product_data)
    return ProductResponse.model_validate(product)
>>>>>>> a1ea5748c597144fda260245ab6181892ce99813
