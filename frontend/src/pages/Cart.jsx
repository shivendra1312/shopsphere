import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { cartAPI } from '../api/cart';
import { Trash2, ShoppingBag } from 'lucide-react';
import './Cart.css';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);

  // 1. Cart data lana
  const fetchCart = async () => {
    try {
      const data = await cartAPI.getCart();
      setCartItems(data);
    } catch (error) {
      console.error("Cart load error:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  // 2. Quantity update (+ ya - button)
  const handleUpdateQuantity = async (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      // Agar 0 ho jaye toh delete kar do
      handleRemoveItem(itemId);
      return;
    }
    try {
      await cartAPI.updateCartItem(itemId, newQuantity);
      fetchCart(); // Refresh karo
    } catch (error) {
      console.error("Update error:", error);
    }
  };

  // 3. Item delete
  const handleRemoveItem = async (itemId) => {
    try {
      await cartAPI.removeFromCart(itemId);
      fetchCart(); // Refresh karo
    } catch (error) {
      console.error("Remove error:", error);
    }
  };

  // 4. Total price calculate (Frontend pe)
  const totalPrice = cartItems.reduce((sum, item) => {
    return sum + (item.product.price * item.quantity);
  }, 0);

  const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  // 5. Loading state
  if (loading) {
    return <div className="cart-page"><h2>Loading your cart...</h2></div>;
  }

  // 6. Empty cart
  if (cartItems.length === 0) {
    return (
      <div className="cart-page">
        <div className="empty-cart">
          <ShoppingBag size={60} />
          <h2>Your cart is empty!</h2>
          <p>Looks like you haven't added anything to your cart yet.</p>
          <Link to="/products" className="shop-link">Start Shopping</Link>
        </div>
      </div>
    );
  }

  // 7. Cart with items
  return (
    <div className="cart-page">
      <h1>Your Cart</h1>

      <div className="cart-items-list">
        {cartItems.map(item => (
          <div key={item.id} className="cart-item">
            <div className="cart-item-info">
              <h3 className="cart-item-title">{item.product.title}</h3>
              <span className="cart-item-category">
                {item.product.category ? item.product.category.name : ''}
              </span>
            </div>

            {/* Quantity Controls: - [qty] + */}
            <div className="quantity-controls">
              <button className="qty-btn" onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}>−</button>
              <span className="qty-value">{item.quantity}</span>
              <button className="qty-btn" onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}>+</button>
            </div>

            <div className="cart-item-price">
              ${(item.product.price * item.quantity).toFixed(2)}
            </div>

            <button className="remove-btn" onClick={() => handleRemoveItem(item.id)} title="Remove">
              <Trash2 size={20} />
            </button>
          </div>
        ))}
      </div>

      {/* Cart Summary */}
      <div className="cart-summary">
        <div className="summary-row">
          <span>Items in cart</span>
          <span>{totalItems}</span>
        </div>
        <div className="summary-row total">
          <span>Total</span>
          <span>${totalPrice.toFixed(2)}</span>
        </div>
        <Link to="/checkout" className="checkout-btn" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
          Proceed to Checkout →
        </Link>
      </div>
    </div>
  );
};

export default Cart;
