from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.categories import router as categories_router
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.wishlist import router as wishlist_router
from app.api.v1.addresses import router as addresses_router
from app.api.v1.orders import router as orders_router
from app.api.v1.payments import router as payments_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.coupons import router as coupons_router

api_v1_router = APIRouter()

# Saare v1 routes yahan add honge
api_v1_router.include_router(auth_router)
api_v1_router.include_router(categories_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(cart_router)
api_v1_router.include_router(wishlist_router)
api_v1_router.include_router(addresses_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(payments_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(reviews_router)
api_v1_router.include_router(coupons_router)