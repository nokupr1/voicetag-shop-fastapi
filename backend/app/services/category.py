from sqlalchemy.ext.asyncio import AsyncSession

<<<<<<< HEAD
from app.schemas.category import CategoryCreate, CategoryResponse
=======
from app.schemas.category import CategoryResponse
>>>>>>> a1ea5748c597144fda260245ab6181892ce99813

from ..repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.category_repository = CategoryRepository(db)

    async def get_all(self) -> list[CategoryResponse]:
        categories = await self.category_repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]

    async def get_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.category_repository.get_by_id(category_id)
        return CategoryResponse.model_validate(category)

<<<<<<< HEAD
    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        category = await self.category_repository.create(category_data)
=======
    async def get_by_slug(self, category_slug: str) -> CategoryResponse:
        category = await self.category_repository.get_by_slug(category_slug)
>>>>>>> a1ea5748c597144fda260245ab6181892ce99813
        return CategoryResponse.model_validate(category)
