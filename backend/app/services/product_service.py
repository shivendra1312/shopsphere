from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.product import Product
from app.schemas.product import ProductCreate

def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 20, 
    search: str = None, 
    category_id: int = None
):
    # 1. Base Query shuru karte hain
    query = db.query(Product)
    
    # 2. Filter logic: Agar category_id aayi hai
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
        
    # 3. Search logic: Agar search keyword aaya hai
    if search:
        # Check if title OR description contains the search word
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.title.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
        
    # 4. Pagination logic: Skip and Limit
    products = query.offset(skip).limit(limit).all()
    return products

def create_product(db: Session, product_in: ProductCreate):
    # Convert schema to SQLAlchemy model
    new_product = Product(
        title=product_in.title,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        category_id=product_in.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
