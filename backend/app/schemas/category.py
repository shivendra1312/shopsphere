from pydantic import BaseModel, Field

# 1. Base Schema (Common fields)
class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    parent_id: int | None = None

# 2. Schema for creating a category (Request)
class CategoryCreate(CategoryBase):
    pass

# 3. Schema for reading a category (Response)
class CategoryResponse(CategoryBase):
    id: int

    model_config = {"from_attributes": True}