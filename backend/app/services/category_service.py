from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.core.redis import get_cache, set_cache, delete_cache

CACHE_KEY_CATEGORIES = "categories:all"

def get_all_categories(db: Session):
    # 1. Check Redis Cache
    cached = get_cache(CACHE_KEY_CATEGORIES)
    if cached is not None:
        return cached

    # 2. Cache miss -> query DB
    categories = db.query(Category).all()
    serialized = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "parent_id": c.parent_id
        }
        for c in categories
    ]

    # 3. Store in cache for 10 minutes
    set_cache(CACHE_KEY_CATEGORIES, serialized, expire_seconds=600)
    return serialized

def create_category(db: Session, category_in: CategoryCreate):
    # Check if category with same name exists
    existing_cat = db.query(Category).filter(Category.name == category_in.name).first()
    if existing_cat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    # Check if parent_id is valid (if provided)
    if category_in.parent_id:
        parent_cat = db.query(Category).filter(Category.id == category_in.parent_id).first()
        if not parent_cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )

    # Convert Pydantic schema to SQLAlchemy model
    new_category = Category(
        name=category_in.name,
        description=category_in.description,
        parent_id=category_in.parent_id
    )

    # Save to DB
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    # Invalidate cache so new category appears immediately
    delete_cache(CACHE_KEY_CATEGORIES)

    return new_category
