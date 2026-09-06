from sqlalchemy import String, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    # 1. Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 2. Basic Info
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 3. Category linking
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    
    # 4. Relationship for Python
    category: Mapped["Category"] = relationship("Category", back_populates="products")