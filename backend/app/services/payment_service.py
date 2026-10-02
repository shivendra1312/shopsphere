import razorpay
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.order import Order, OrderStatus

# Razorpay client initialize karna
# Agar keys nahi hain, toh development mode me payment bypass kar sakte hain
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment_order(db: Session, order_id: int, user_id: int):
    # 1. Apna Order find karo
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if db_order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order is already paid or cancelled")

    # 2. Amount ko paise (Indian Rupees) me convert karna (Razorpay rule: amount * 100)
    # USD me hai toh bhi logic waise hi chalega, standard smallest unit. 
    amount_in_paise = int(db_order.total_amount * 100)

    # 3. Razorpay ka API call karke order create karna
    try:
        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"receipt_order_{db_order.id}",
            "notes": {
                "order_id": db_order.id,
                "user_id": user_id
            }
        })
        
        # Ye frontend ko bhejna hota hai
        return {
            "id": razorpay_order['id'],
            "amount": razorpay_order['amount'],
            "currency": razorpay_order['currency']
        }
    except Exception as e:
        print("Razorpay error:", e)
        raise HTTPException(status_code=500, detail="Payment gateway error")

def verify_payment_signature(db: Session, order_id: int, user_id: int, rzp_order_id: str, rzp_payment_id: str, signature: str):
    # 1. Signature verify karna using Razorpay utility
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': rzp_order_id,
            'razorpay_payment_id': rzp_payment_id,
            'razorpay_signature': signature
        })
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Payment signature verification failed. Fake payment!")

    # 2. Agar pass ho gaya, toh database me order update kardo
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    db_order.status = OrderStatus.PAID
    db_order.payment_id = rzp_payment_id
    db.commit()
    
    return {"status": "success", "message": "Payment verified successfully!"}
