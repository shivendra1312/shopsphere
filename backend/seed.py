import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.category import Category
from app.models.product import Product

def seed_db():
    db = SessionLocal()
    try:
        # Check if categories exist
        if db.query(Category).count() == 0:
            print("Categories nahi mili, nayi bana raha hu...")
            electronics = Category(name="Electronics", description="Gadgets and devices")
            clothing = Category(name="Clothing", description="Apparel and fashion")
            db.add_all([electronics, clothing])
            db.commit()
            db.refresh(electronics)
            db.refresh(clothing)
            
            print("Products add kar raha hu...")
            p1 = Product(title="iPhone 15 Pro", description="Latest Apple iPhone with titanium body.", price=999.99, stock=50, category_id=electronics.id)
            p2 = Product(title="MacBook Air M2", description="Super fast laptop for professionals.", price=1199.50, stock=20, category_id=electronics.id)
            p3 = Product(title="Sony WH-1000XM5", description="Noise cancelling headphones.", price=348.00, stock=5, category_id=electronics.id)
            p4 = Product(title="Levi's 511 Jeans", description="Classic slim fit jeans.", price=59.99, stock=100, category_id=clothing.id)
            p5 = Product(title="Nike Air Force 1", description="Iconic white sneakers.", price=110.00, stock=0, category_id=clothing.id)
            
            db.add_all([p1, p2, p3, p4, p5])
            db.commit()
            print("Successfully added 2 categories and 5 products!")
        else:
            print("Database me already products hain.")

        # Seed initial test coupons
        from app.models.coupon import Coupon
        if db.query(Coupon).count() == 0:
            print("Coupons add kar raha hu...")
            c1 = Coupon(code="SAVE10", discount_percent=10.0, min_order_amount=0.0)
            c2 = Coupon(code="WELCOME20", discount_percent=20.0, min_order_amount=100.0)
            c3 = Coupon(code="SHOPSPHERE50", discount_percent=50.0, min_order_amount=500.0)
            db.add_all([c1, c2, c3])
            db.commit()
            print("Coupons SAVE10, WELCOME20, SHOPSPHERE50 added!")
    except Exception as e:
        print("Error aaya:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
