from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository
from ..schemas.product import ProductCreate, ProductListResponse, ProductResponse


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    async def get_all(self) -> ProductListResponse:
        products = await self.product_repository.get_all()
        result = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=result, total=len(result))

    async def get_by_id(self, product_id: int) -> ProductResponse:
        product = await self.product_repository.get_by_id(product_id)
        return ProductResponse.model_validate(product)

    async def get_multiple_by_ids(self, products_ids: list[int]) -> ProductListResponse:
        products = await self.product_repository.get_multiple_by_ids(products_ids)
        result = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=result, total=len(result))

    async def get_by_category(self, category_id: int) -> ProductListResponse:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        products = await self.product_repository.get_by_category(category_id)
        result = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=result, total=len(result))

    async def create(self, data: ProductCreate) -> ProductResponse:
        product = await self.product_repository.create(data)
        return ProductResponse.model_validate(product)
