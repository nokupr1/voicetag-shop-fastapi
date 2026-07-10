from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Numeric

from ..database import Base

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), index=True)
    image_url: Mapped[Optional[str]]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    category: Mapped["Category"] = relationship(back_populates="products")
