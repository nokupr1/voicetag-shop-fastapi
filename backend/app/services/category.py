from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.category import CategoryResponse

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

    async def get_by_slug(self, category_slug: str) -> CategoryResponse:
        category = await self.category_repository.get_by_slug(category_slug)
        return CategoryResponse.model_validate(category)
