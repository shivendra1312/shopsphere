import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { productsAPI } from '../api/products';
import './ProductDetail.css';

const ProductDetail = () => {
  // 1. URL se ID nikalna
  const { id } = useParams();
  
  // 2. State variables
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  // 3. Data lana
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await productsAPI.getProduct(id);
        setProduct(data);
      } catch (error) {
        console.error("Product nahi mila", error);
      }
      setLoading(false);
    };

    fetchProduct();
  }, [id]); // Agar ID badle toh naya data lao

  // 4. Loading state
  if (loading) {
    return <div className="product-detail-page"><h2>Loading product details...</h2></div>;
  }

  // 5. Agar API ne error diya (e.g. invalid ID)
  if (!product) {
    return <div className="product-detail-page"><h2>Product not found!</h2></div>;
  }

  return (
    <div className="product-detail-page">
      <div className="detail-card">
        
        <span className="detail-category">
          {product.category ? product.category.name : 'Uncategorized'}
        </span>
        
        <h1 className="detail-title">{product.title}</h1>
        
        <div className="detail-description">
          {product.description}
        </div>
        
        <div className="detail-bottom">
          <div className="detail-price">${product.price.toFixed(2)}</div>
          
          <button 
            className="add-to-cart-btn" 
            disabled={product.stock === 0}
          >
            {product.stock === 0 ? "Out of Stock" : "Add to Cart"}
          </button>
        </div>
        
        <div style={{ color: product.stock < 5 ? '#ecc94b' : '#a0aec0', fontSize: '0.9rem' }}>
          {product.stock > 0 ? `${product.stock} items available in stock` : 'Currently unavailable'}
        </div>

      </div>
    </div>
  );
};

export default ProductDetail;
