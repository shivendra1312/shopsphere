from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    # Basic columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Sub-category logic (Self-referential)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    # Relationships (SQLAlchemy ke use ke liye)
    subcategories: Mapped[list["Category"]] = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped["Category"] = relationship("Category", back_populates="subcategories", remote_side=[id])
    
    # Relationship with products
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category", cascade="all, delete-orphan")