from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category import Category
from ..schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Category]:
        statement = select(Category)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category:
        statement = select(Category).filter(Category.id == category_id)
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return category

    async def get_by_slug(self, category_slug: str) -> Category:
        statement = select(Category).filter(Category.slug == category_slug)
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with slug {category_slug} not found",
            )
        return category

    async def create(self, category_data: CategoryCreate) -> Category:
        try:
            category = Category(**category_data.model_dump())
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
            return category
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {category_data.name} or slug {category_data.slug} already exists",
            )
