from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("", response_model=List[CartItemResponse])
def get_user_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all items in the current logged in user's cart.
    """
    return cart_service.get_cart(db, current_user.id)

@router.post("", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(item_in: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Add a product to the cart or increase its quantity.
    """
    return cart_service.add_to_cart(db, current_user.id, item_in)

@router.put("/{item_id}", response_model=CartItemResponse)
def update_item_quantity(item_id: int, item_in: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update the quantity of an item in the cart. If 0, it gets deleted.
    """
    updated_item = cart_service.update_cart_item(db, current_user.id, item_id, item_in.quantity)
    if not updated_item and item_in.quantity > 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if not updated_item: # Item deleted due to 0 quantity
        return CartItemResponse(id=item_id, user_id=current_user.id, product_id=0, quantity=0, product=None) # Returning dummy on delete
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove a specific item from the cart.
    """
    cart_service.remove_from_cart(db, current_user.id, item_id)
    return None

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_user_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove ALL items from the user's cart (used after checkout).
    """
    cart_service.clear_cart(db, current_user.id)
    return None
