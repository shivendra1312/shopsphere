from sqlalchemy.orm import Session
from app.models.wishlist import WishlistItem
from app.models.product import Product
from app.schemas.wishlist import WishlistItemCreate
from fastapi import HTTPException

def get_wishlist(db: Session, user_id: int):
    return db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()

def add_to_wishlist(db: Session, user_id: int, item_in: WishlistItemCreate):
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.product_id == item_in.product_id
    ).first()

    if existing_item:
        # Wishlist me quantity nahi hoti, agar pehle se hai toh wahi wapas bhej do
        return existing_item
        
    new_item = WishlistItem(
        user_id=user_id,
        product_id=item_in.product_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def remove_from_wishlist(db: Session, user_id: int, item_id: int):
    item = db.query(WishlistItem).filter(WishlistItem.id == item_id, WishlistItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
    return True
