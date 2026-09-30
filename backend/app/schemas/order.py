from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.product import ProductResponse
from app.schemas.address import AddressResponse

class OrderCreate(BaseModel):
    # Jab order create hota hai toh sirf address ki id chahiye, cart se items backend khud uthayega!
    address_id: int 

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    price: float
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: Optional[int]
    total_amount: float
    status: OrderStatus
    payment_id: Optional[str]
    created_at: datetime
    
    # Ye order_response me pura address aur saare items daal dega
    address: Optional[AddressResponse] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
