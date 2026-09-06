from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import UserRole
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories. Anyone can view categories.
    """
    return category_service.get_all_categories(db)


@router.post("", response_model=CategoryResponse, status_code=201, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category. Only ADMIN can do this.
    """
    return category_service.create_category(db, category_in)
