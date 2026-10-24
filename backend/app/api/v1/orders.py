from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service
from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["Orders"])

class StatusUpdate(BaseModel):
    status: OrderStatus

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, "ADMIN"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return order_service.create_order(db, current_user.id, order_in.address_id)

@router.get("", response_model=List[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return order_service.get_user_orders(db, current_user.id)

@router.get("/all", response_model=List[OrderResponse])
def admin_get_all_orders(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Admin only: Get ALL orders from all users"""
    return order_service.get_all_orders(db)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def admin_update_status(order_id: int, body: StatusUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Admin only: Update order status (PENDING → SHIPPED → DELIVERED)"""
    return order_service.update_order_status(db, order_id, body.status)
