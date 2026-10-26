from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate

def get_product_reviews(db: Session, product_id: int):
    return db.query(Review).filter(Review.product_id == product_id).order_by(Review.created_at.desc()).all()

def get_product_rating_summary(db: Session, product_id: int):
    stats = db.query(
        func.avg(Review.rating).label("avg_rating"),
        func.count(Review.id).label("total_reviews")
    ).filter(Review.product_id == product_id).first()

    avg_val = float(stats.avg_rating) if stats and stats.avg_rating else 0.0
    count_val = int(stats.total_reviews) if stats and stats.total_reviews else 0

    return {
        "average_rating": round(avg_val, 1),
        "total_reviews": count_val
    }

def create_or_update_review(db: Session, user_id: int, product_id: int, review_in: ReviewCreate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    existing_review = db.query(Review).filter(
        Review.user_id == user_id,
        Review.product_id == product_id
    ).first()

    if existing_review:
        existing_review.rating = review_in.rating
        existing_review.comment = review_in.comment
        db.commit()
        db.refresh(existing_review)
        return existing_review

    new_review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=review_in.rating,
        comment=review_in.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def delete_review(db: Session, user_id: int, review_id: int, is_admin: bool = False):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    if review.user_id != user_id and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this review")

    db.delete(review)
    db.commit()
    return True
