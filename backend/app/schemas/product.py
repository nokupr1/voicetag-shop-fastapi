from decimal import Decimal

from pydantic import BaseModel, Field

from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(min_length=5, description="Product name")
    description: str | None = Field(
        default=None, max_length=255, description="Product description"
    )
    price: Decimal = Field(gt=0, description="Product price")
    image_url: str | None = Field(default=None, description="Product image URL")
    category_id: int = Field(gt=0, description="Product category identifier")


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int = Field(gt=0, description="Product identifier")
    category: CategoryResponse = Field(description="Product category details")
    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(ge=0, description="Total number of products")
