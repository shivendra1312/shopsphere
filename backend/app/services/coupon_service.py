from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate

def apply_coupon(db: Session, code: str, order_amount: float):
    clean_code = code.strip().upper()
    coupon = db.query(Coupon).filter(Coupon.code == clean_code).first()

    if not coupon or not coupon.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired coupon code"
        )

    if order_amount < coupon.min_order_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Coupon requires a minimum order amount of ${coupon.min_order_amount:.2f}"
        )

    discount_amount = round((order_amount * coupon.discount_percent) / 100.0, 2)
    final_amount = max(0.0, round(order_amount - discount_amount, 2))

    return {
        "valid": True,
        "code": coupon.code,
        "discount_percent": coupon.discount_percent,
        "discount_amount": discount_amount,
        "final_amount": final_amount,
        "message": f"Coupon applied! You saved ${discount_amount:.2f} ({coupon.discount_percent}%)"
    }

def create_coupon(db: Session, coupon_in: CouponCreate):
    clean_code = coupon_in.code.strip().upper()
    existing = db.query(Coupon).filter(Coupon.code == clean_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon code already exists"
        )

    new_coupon = Coupon(
        code=clean_code,
        discount_percent=coupon_in.discount_percent,
        min_order_amount=coupon_in.min_order_amount,
        is_active=coupon_in.is_active
    )
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return new_coupon

def get_all_coupons(db: Session):
    return db.query(Coupon).order_by(Coupon.created_at.desc()).all()
