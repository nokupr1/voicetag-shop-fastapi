from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository
from ..schemas.product import ProductCreate, ProductListResponse, ProductResponse


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        product = await self.product_repository.create(data)
        return ProductResponse.model_validate(product)

    async def get_all_products(self) -> ProductListResponse:
        products = await self.product_repository.get_all()
        result = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=result, total=len(result))

    async def delete_product(self, product_id: int) -> ProductResponse:
        product = await self.product_repository.delete(product_id)
        return ProductResponse.model_validate(product)
