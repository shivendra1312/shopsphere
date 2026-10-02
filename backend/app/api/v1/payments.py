from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentVerify
from app.services import payment_service
from app.core.config import settings

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-order")
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a Razorpay order id for a given database order.
    Frontend needs this ID to open the Razorpay popup.
    """
    return payment_service.create_payment_order(db, payment_in.order_id, current_user.id)

@router.post("/verify")
def verify_payment(verify_in: PaymentVerify, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Verifies the payment after the user pays in the Razorpay popup.
    """
    return payment_service.verify_payment_signature(
        db=db,
        order_id=verify_in.order_id,
        user_id=current_user.id,
        rzp_order_id=verify_in.razorpay_order_id,
        rzp_payment_id=verify_in.razorpay_payment_id,
        signature=verify_in.razorpay_signature
    )
    
@router.get("/key")
def get_razorpay_key(current_user: User = Depends(get_current_user)):
    """
    Frontend needs the public key to load the Razorpay checkout.
    """
    return {"key": settings.RAZORPAY_KEY_ID}
