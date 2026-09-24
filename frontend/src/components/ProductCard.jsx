import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const navigate = useNavigate();

  // Stock ke hisaab se color class decide karo
  let stockClass = "in-stock";
  let stockText = "In Stock";
  
  if (product.stock === 0) {
    stockClass = "out-of-stock";
    stockText = "Out of Stock";
  } else if (product.stock < 5) {
    stockClass = "low-stock";
    stockText = `Only ${product.stock} left`;
  }

  // Jab card pe click ho, toh detail page pe le jao
  const handleClick = () => {
    navigate(`/products/${product.id}`);
  };

  return (
    <div className="product-card" onClick={handleClick}>
      <span className="product-category">
        {product.category ? product.category.name : 'Uncategorized'}
      </span>
      
      <h3 className="product-title">{product.title}</h3>
      
      <div className="product-price">
        ${product.price.toFixed(2)}
      </div>
      
      <div className="product-stock">
        <span className={`stock-indicator ${stockClass}`}></span>
        {stockText}
      </div>
    </div>
  );
};

export default ProductCard;
