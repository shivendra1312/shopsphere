import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { wishlistAPI, cartAPI } from '../api/cart';
import { Trash2, Heart, ShoppingCart } from 'lucide-react';
import './Wishlist.css';

const Wishlist = () => {
  const [wishlistItems, setWishlistItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchWishlist = async () => {
    try {
      const data = await wishlistAPI.getWishlist();
      setWishlistItems(data);
    } catch (error) {
      console.error("Wishlist load error:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const handleRemove = async (itemId) => {
    try {
      await wishlistAPI.removeFromWishlist(itemId);
      fetchWishlist(); // Refresh list
    } catch (error) {
      console.error("Remove error:", error);
    }
  };

  const handleMoveToCart = async (productId, itemId) => {
    try {
      // 1. Cart me daalo
      await cartAPI.addToCart(productId, 1);
      // 2. Wishlist se hatao
      await handleRemove(itemId);
    } catch (error) {
      console.error("Move to cart error:", error);
    }
  };

  if (loading) {
    return <div className="wishlist-page"><h2>Loading your wishlist...</h2></div>;
  }

  if (wishlistItems.length === 0) {
    return (
      <div className="wishlist-page">
        <div className="empty-wishlist">
          <Heart size={60} color="#fc8181" />
          <h2>Your Wishlist is empty!</h2>
          <p>Save items you like here to buy them later.</p>
          <Link to="/products" className="shop-link">Explore Products</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="wishlist-page">
      <h1><Heart size={28} color="#fc8181" style={{ display: 'inline', marginRight: '10px' }} /> My Wishlist</h1>

      <div className="wishlist-grid">
        {wishlistItems.map(item => (
          <div key={item.id} className="wishlist-card">
            
            {/* Image Placeholder */}
            <div className="wishlist-img-placeholder">
              <span>{item.product.title.charAt(0)}</span>
            </div>

            <div className="wishlist-card-content">
              <h3>{item.product.title}</h3>
              <p className="price">${item.product.price.toFixed(2)}</p>
              
              <div className="wishlist-actions">
                <button 
                  className="move-to-cart-btn" 
                  onClick={() => handleMoveToCart(item.product.id, item.id)}
                  disabled={item.product.stock === 0}
                >
                  <ShoppingCart size={16} /> 
                  {item.product.stock === 0 ? "Out of Stock" : "Move to Cart"}
                </button>
                <button 
                  className="delete-wishlist-btn" 
                  onClick={() => handleRemove(item.id)}
                  title="Remove from Wishlist"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Wishlist;
