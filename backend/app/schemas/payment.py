from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int

class PaymentVerify(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
