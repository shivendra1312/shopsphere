import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI } from '../api/products';
import ProductCard from '../components/ProductCard';
import './Home.css';

const Home = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Home page par hum sirf pehle 4 ya 8 products dikhayenge
  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        // limit=4 bhej rahe hain taaki sirf 4 products aayen
        const data = await productsAPI.getProducts({ limit: 4 });
        setFeaturedProducts(data);
      } catch (error) {
        console.error("Featured products nahi aaye", error);
      }
      setLoading(false);
    };

    fetchFeatured();
  }, []);

  return (
    <div className="home-page">
      {/* 1. Hero Section (Big Banner) */}
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">ShopSphere</h1>
          <p className="hero-subtitle">Discover premium products at unbeatable prices.</p>
          <Link to="/products" className="shop-now-btn">
            Shop Now
          </Link>
        </div>
      </div>

      {/* 2. Featured Products Section */}
      <div className="featured-section">
        <h2 className="section-title">Featured Products</h2>
        
        {loading ? (
          <div style={{ textAlign: 'center', color: '#fff' }}>Loading featured items...</div>
        ) : (
          <div className="featured-grid">
            {featuredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
