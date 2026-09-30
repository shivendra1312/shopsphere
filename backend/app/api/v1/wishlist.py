from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.wishlist import WishlistItemCreate, WishlistItemResponse
from app.services import wishlist_service

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.get("", response_model=List[WishlistItemResponse])
def get_user_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all items in the current logged in user's wishlist.
    """
    return wishlist_service.get_wishlist(db, current_user.id)

@router.post("", response_model=WishlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_wishlist(item_in: WishlistItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Add a product to the wishlist.
    """
    return wishlist_service.add_to_wishlist(db, current_user.id, item_in)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_wishlist(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove a specific item from the wishlist.
    """
    wishlist_service.remove_from_wishlist(db, current_user.id, item_id)
    return None
