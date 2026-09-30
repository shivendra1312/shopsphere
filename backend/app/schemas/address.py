from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    full_name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    is_default: Optional[bool] = False

class AddressResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    is_default: bool

    class Config:
        from_attributes = True
