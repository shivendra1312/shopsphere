from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CouponCreate(BaseModel):
    code: str
    discount_percent: float = Field(..., ge=1.0, le=100.0)
    min_order_amount: float = Field(default=0.0, ge=0.0)
    is_active: bool = True

class CouponApply(BaseModel):
    code: str
    order_amount: float

class CouponResponse(BaseModel):
    id: int
    code: str
    discount_percent: float
    min_order_amount: float
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class CouponApplyResult(BaseModel):
    valid: bool
    code: str
    discount_percent: float
    discount_amount: float
    final_amount: float
    message: str
