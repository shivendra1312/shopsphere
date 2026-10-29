from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import UserRole
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0, description="Kitne products skip karne hain (Pagination)"),
    limit: int = Query(20, ge=1, le=100, description="Ek page me kitne products dikhane hain"),
    search: Optional[str] = Query(None, description="Naam ya description me search karne ke liye"),
    category_id: Optional[int] = Query(None, description="Category ke hisaab se filter karne ke liye"),
    db: Session = Depends(get_db)
):
    """
    Get all products with optional searching, filtering, and pagination.
    Anyone can view products.
    """
    return product_service.get_products(
        db=db, 
        skip=skip, 
        limit=limit, 
        search=search, 
        category_id=category_id
    )

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by its ID.
    """
    from fastapi import HTTPException
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductResponse, status_code=201, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product. Only ADMIN can do this.
    """
    return product_service.create_product(db, product_in)

@router.delete("/{product_id}", status_code=204, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product. Only ADMIN can do this.
    """
    from fastapi import HTTPException
    deleted = product_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
