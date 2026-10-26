from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services import review_service

router = APIRouter(tags=["Reviews"])

@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific product"""
    return review_service.get_product_reviews(db, product_id)

@router.get("/products/{product_id}/reviews/summary")
def get_rating_summary(product_id: int, db: Session = Depends(get_db)):
    """Get average rating and total review count for a product"""
    return review_service.get_product_rating_summary(db, product_id)

@router.post("/products/{product_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def submit_review(
    product_id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Customer submits or updates their review for a product"""
    return review_service.create_or_update_review(db, current_user.id, product_id, review_in)

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review (own review or admin)"""
    is_admin = current_user.role in [UserRole.ADMIN, "ADMIN"]
    review_service.delete_review(db, current_user.id, review_id, is_admin=is_admin)
    return None
