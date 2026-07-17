from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models.category import Category
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Product]:
        statement = select(Product).options(joinedload(Product.category))
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int) -> Product:
        statement = (
            select(Product)
            .filter(Product.id == product_id)
            .options(joinedload(Product.category))
        )
        result = await self.session.execute(statement)
        product = result.scalar_one_or_none()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )
        return product

    async def get_by_category(self, category_id: int) -> list[Product]:
        category = await self.session.execute(
            select(Category).filter(Category.id == category_id)
        )
        if category.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        statement = (
            select(Product)
            .filter(Product.category_id == category_id)
            .options(joinedload(Product.category))
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        statement = (
            select(Product)
            .filter(Product.id.in_(product_ids))
            .options(joinedload(Product.category))
        )
        result = await self.session.execute(statement)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found with the given ids",
            )
        return list(result.scalars().all())

    async def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return await self.get_by_id(product.id)
