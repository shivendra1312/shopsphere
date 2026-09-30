from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductResponse

# Jab user product add karega cart me
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

# Jab user cart me quantity change karega (e.g. + ya - dabana)
class CartItemUpdate(BaseModel):
    quantity: int

# Jab API cart ka data wapas bhejegi
class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: ProductResponse  # Ye line magic hai! Isse frontend ko direct product ki image aur price mil jayegi

    class Config:
        from_attributes = True
