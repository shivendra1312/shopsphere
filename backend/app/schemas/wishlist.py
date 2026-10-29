from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductResponse

# Jab user product wishlist me daalega
class WishlistItemCreate(BaseModel):
    product_id: int

# Jab API wishlist ka data wapas bhejegi
class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: ProductResponse  # Product details include karenge

    model_config = {"from_attributes": True}
