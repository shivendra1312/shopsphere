from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.models.product import Product
from app.core.redis import get_cache, set_cache

CACHE_KEY_DASHBOARD = "dashboard:stats"

def get_dashboard_stats(db: Session):
    cached = get_cache(CACHE_KEY_DASHBOARD)
    if cached is not None:
        return cached

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
    serialized_orders = [
        {
            "id": o.id,
            "user_id": o.user_id,
            "total_amount": o.total_amount,
            "status": str(o.status.value if hasattr(o.status, 'value') else o.status),
            "created_at": o.created_at.isoformat() if o.created_at else None
        }
        for o in recent_orders
    ]

    stats_data = {
        "revenue": round(revenue, 2),
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "total_users": total_users,
        "total_products": total_products,
        "recent_orders": serialized_orders
    }

    # Cache for 60 seconds
    set_cache(CACHE_KEY_DASHBOARD, stats_data, expire_seconds=60)
    return stats_data
