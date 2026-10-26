from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.schemas.coupon import CouponCreate, CouponApply, CouponResponse, CouponApplyResult
from app.services import coupon_service

router = APIRouter(prefix="/coupons", tags=["Coupons"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, "ADMIN"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.post("/apply", response_model=CouponApplyResult)
def apply_coupon_code(payload: CouponApply, db: Session = Depends(get_db)):
    """Apply and validate a coupon on a given order amount"""
    return coupon_service.apply_coupon(db, payload.code, payload.order_amount)

@router.post("", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
def create_new_coupon(
    coupon_in: CouponCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin only: Create a new discount coupon"""
    return coupon_service.create_coupon(db, coupon_in)

@router.get("", response_model=List[CouponResponse])
def get_coupons(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin only: View all coupons"""
    return coupon_service.get_all_coupons(db)
