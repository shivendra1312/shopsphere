import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { cartAPI } from '../api/cart';
import { checkoutAPI } from '../api/checkout';
import './Checkout.css';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState('');
  const [orderSuccess, setOrderSuccess] = useState(null); // Order successful hone par order object store hoga

  // Address form state
  const [address, setAddress] = useState({
    full_name: '',
    phone: '',
    street: '',
    city: '',
    state: '',
    zip_code: ''
  });

  // Cart data fetch karna
  useEffect(() => {
    const fetchCart = async () => {
      try {
        const data = await cartAPI.getCart();
        setCartItems(data);
      } catch (err) {
        setError('Cart load nahi hua. Wapas try karo.');
      }
      setLoading(false);
    };
    fetchCart();
  }, []);

  // Total price calculate karna
  const totalPrice = cartItems.reduce((sum, item) => {
    return sum + (item.product.price * item.quantity);
  }, 0);

  // Form field update karna
  const handleChange = (e) => {
    setAddress({ ...address, [e.target.name]: e.target.value });
  };

  // Place Order ka logic
  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    setError('');

    // Basic validation
    for (const key of Object.keys(address)) {
      if (!address[key].trim()) {
        setError('Please fill all address fields.');
        return;
      }
    }

    setPlacing(true);
    try {
      // Step 1: Address save karo, uska ID milega
      const savedAddress = await checkoutAPI.addAddress(address);

      // Step 2: Us address ke saath order create karo
      const order = await checkoutAPI.createOrder(savedAddress.id);

      // Step 3: Payment simulate karna (Razorpay skip)
      setOrderSuccess(order);
    } catch (err) {
      const msg = err.response?.data?.detail || 'Order place nahi hua. Wapas try karo.';
      setError(msg);
    }
    setPlacing(false);
  };

  // --- Order Success Screen ---
  if (orderSuccess) {
    return (
      <div className="checkout-page">
        <div className="order-success">
          <div className="success-icon">🎉</div>
          <h2>Order Placed Successfully!</h2>
          <p>Tumhara order confirm ho gaya hai. Jald hi deliver hoga!</p>
          <div className="order-id">Order #{orderSuccess.id} · ₹{orderSuccess.total_amount.toFixed(2)}</div>
          <br />
          <Link to="/products" className="continue-shopping">Continue Shopping</Link>
        </div>
      </div>
    );
  }

  // --- Loading ---
  if (loading) return <div className="checkout-page"><h2>Loading...</h2></div>;

  // --- Empty Cart ---
  if (cartItems.length === 0) {
    return (
      <div className="checkout-page">
        <div className="order-success">
          <div className="success-icon">🛒</div>
          <h2>Cart khali hai!</h2>
          <p>Pehle kuch products add karo.</p>
          <Link to="/products" className="continue-shopping">Shop Now</Link>
        </div>
      </div>
    );
  }

  // --- Main Checkout Page ---
  return (
    <div className="checkout-page">
      <h1>Checkout</h1>

      <form onSubmit={handlePlaceOrder}>
        <div className="checkout-grid">

          {/* LEFT: Delivery Address Form */}
          <div className="address-section">
            <h2>📍 Delivery Address</h2>

            <div className="form-row">
              <div className="form-group">
                <label>Full Name</label>
                <input
                  name="full_name"
                  placeholder="Rahul Sharma"
                  value={address.full_name}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Phone Number</label>
                <input
                  name="phone"
                  placeholder="9876543210"
                  value={address.phone}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group full-width">
              <label>Street Address</label>
              <input
                name="street"
                placeholder="12, Gandhi Nagar, Near Bus Stand"
                value={address.street}
                onChange={handleChange}
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>City</label>
                <input
                  name="city"
                  placeholder="Jaipur"
                  value={address.city}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>State</label>
                <input
                  name="state"
                  placeholder="Rajasthan"
                  value={address.state}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>PIN Code</label>
              <input
                name="zip_code"
                placeholder="302001"
                value={address.zip_code}
                onChange={handleChange}
              />
            </div>

            {error && <div className="error-msg">⚠️ {error}</div>}
          </div>

          {/* RIGHT: Order Summary */}
          <div className="order-summary">
            <h2>🧾 Order Summary</h2>

            {cartItems.map(item => (
              <div key={item.id} className="summary-item">
                <span>{item.product.title} × {item.quantity}</span>
                <span>${(item.product.price * item.quantity).toFixed(2)}</span>
              </div>
            ))}

            <div className="summary-total">
              <span>Total</span>
              <span>${totalPrice.toFixed(2)}</span>
            </div>

            <button
              type="submit"
              className="place-order-btn"
              disabled={placing}
            >
              {placing ? '⏳ Placing Order...' : '✅ Place Order'}
            </button>
          </div>

        </div>
      </form>
    </div>
  );
};

export default Checkout;
