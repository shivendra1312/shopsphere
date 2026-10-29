from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewUser(BaseModel):
    id: int
    first_name: Optional[str] = None
    email: str

    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1)

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime
    user: Optional[ReviewUser] = None

    model_config = {"from_attributes": True}
