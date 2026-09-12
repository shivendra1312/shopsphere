from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.category import CategoryResponse

# 1. Base Schema
class ProductBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int

# 2. Schema for creating a product (Request)
class ProductCreate(ProductBase):
    pass

# 3. Schema for reading a product (Response)
class ProductResponse(ProductBase):
    id: int
    
    # Nested Schema: Taki frontend ko category ka naam bhi mil jaye
    category: Optional[CategoryResponse] = None

    model_config = {"from_attributes": True}