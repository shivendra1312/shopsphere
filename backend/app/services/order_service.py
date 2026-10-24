from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.address import Address
from fastapi import HTTPException

def create_order(db: Session, user_id: int, address_id: int):
    # 1. Cart items check karo
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart khali hai, order nahi ban sakta.")

    # 2. Address verify karo
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address invalid hai.")

    # 3. Total amount calculate karo aur Stock check karo
    total = 0.0
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"'{item.product.title}' ka stock khatam ho gaya!")
        total += item.product.price * item.quantity

    # 4. Order table me entry banao
    new_order = Order(
        user_id=user_id,
        address_id=address_id,
        total_amount=total,
        status=OrderStatus.PENDING
    )
    db.add(new_order)
    db.commit() # id generate karne ke liye commit
    db.refresh(new_order)

    # 5. OrderItems table me entry banao aur product stock minus karo
    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price # Aaj jo price hai wahi lock kar rahe hain
        )
        db.add(order_item)
        
        # Stock minus karna
        item.product.stock -= item.quantity

    # 6. User ki cart khali kardo
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    
    db.commit()
    db.refresh(new_order)
    
    return new_order

def get_user_orders(db: Session, user_id: int):
    # User ko uske saare orders dikhane ke liye (Order History)
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

def get_all_orders(db: Session):
    # Admin ke liye: platform ke SAARE orders
    return db.query(Order).order_by(Order.created_at.desc()).all()

def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
