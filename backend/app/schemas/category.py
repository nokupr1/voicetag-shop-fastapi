from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=5, description="Category name")
    slug: str = Field(min_length=5, description="Category slug")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int = Field(gt=0, description="Category identifier")
    model_config = {"from_attributes": True}


class CategoryListResponse(BaseModel):
    categories: list[CategoryResponse]
    total: int = Field(ge=0, description="Total number of categories")
