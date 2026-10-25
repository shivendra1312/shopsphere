from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.models.product import Product

def get_dashboard_stats(db: Session):
    # 1. Total Revenue (sirf PAID/DELIVERED orders se)
    revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status.in_([OrderStatus.PAID, OrderStatus.DELIVERED])
    ).scalar() or 0.0

    # 2. Total Orders
    total_orders = db.query(func.count(Order.id)).scalar() or 0

    # 3. Orders by status
    pending_orders = db.query(func.count(Order.id)).filter(Order.status == OrderStatus.PENDING).scalar() or 0
    shipped_orders = db.query(func.count(Order.id)).filter(Order.status == OrderStatus.SHIPPED).scalar() or 0

    # 4. Total Users
    total_users = db.query(func.count(User.id)).scalar() or 0

    # 5. Total Products
    total_products = db.query(func.count(Product.id)).scalar() or 0

    # 6. Recent 5 orders
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()

    return {
        "revenue": round(revenue, 2),
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "total_users": total_users,
        "total_products": total_products,
        "recent_orders": recent_orders
    }
