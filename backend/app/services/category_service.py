from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.schemas.category import CategoryCreate

def get_all_categories(db: Session):
    return db.query(Category).all()

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
    
    return new_category
