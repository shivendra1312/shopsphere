from sqlalchemy.orm import Session
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate
from fastapi import HTTPException

def get_cart(db: Session, user_id: int):
    # User ka sara cart items lao (saath me unke linked product details bhi aa jayenge relationship ki wajah se)
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, item_in: CartItemCreate):
    # 1. Pehle check karo product exist karta hai ya nahi
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Check karo kya ye product pehle se cart me hai?
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == item_in.product_id
    ).first()

    if existing_item:
        # Agar hai, toh bas uski quantity badha do
        existing_item.quantity += item_in.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Agar nahi hai, toh naya daal do
        new_item = CartItem(
            user_id=user_id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
        
    if quantity <= 0:
        # Agar quantity 0 kardi, toh seedha delete kardo!
        db.delete(item)
        db.commit()
        return None
        
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item

def remove_from_cart(db: Session, user_id: int, item_id: int):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
    return True

def clear_cart(db: Session, user_id: int):
    # Checkout ke baad cart khali karne ke kaam aayega
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return True
