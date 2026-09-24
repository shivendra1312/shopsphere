import React, { useState, useEffect } from 'react';
import { productsAPI, categoriesAPI } from '../api/products';
import ProductCard from '../components/ProductCard';
import Pagination from '../components/Pagination';
import './Products.css';

const Products = () => {
  // 1. State Variables
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters State
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  
  // Pagination State
  const [page, setPage] = useState(1);
  const limit = 20; // 20 items per page

  // 2. Fetch Data Logic
  const fetchInitialData = async () => {
    try {
      // API Call: Fetch Categories
      const cats = await categoriesAPI.getCategories();
      setCategories(cats);
    } catch (error) {
      console.error("Categories nahi aayi", error);
    }
  };

  const fetchProducts = async () => {
    setLoading(true);
    try {
      // Filter logic build karna
      const params = {
        limit: limit,
        skip: (page - 1) * limit
      };
      if (search) params.search = search;
      if (selectedCategory) params.category_id = selectedCategory;

      // API Call: Fetch Products with filters
      const data = await productsAPI.getProducts(params);
      setProducts(data);
    } catch (error) {
      console.error("Products lane me error", error);
    }
    setLoading(false);
  };

  // 3. useEffect (Page Load par)
  useEffect(() => {
    fetchInitialData();
  }, []);

  // 4. useEffect (Jab bhi search, category, ya PAGE badle)
  useEffect(() => {
    // Thoda delay (debouncing) laga sakte hain baad me, abhi seedha call
    const delay = setTimeout(() => {
      fetchProducts();
    }, 500); // User ko type karne ka 0.5s do, phir API call karo
    
    return () => clearTimeout(delay);
  }, [search, selectedCategory, page]);

  // Reset page to 1 if search or category changes
  useEffect(() => {
    setPage(1);
  }, [search, selectedCategory]);

  // 5. Render UI
  return (
    <div className="products-page">
      <div className="page-header">
        <h1>All Products</h1>
      </div>

      <div className="filters-bar">
        <input 
          type="text" 
          placeholder="Search products..." 
          className="search-input"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        
        <select 
          className="category-select" 
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="loading-state">Loading amazing products...</div>
      ) : products.length === 0 ? (
        <div className="empty-state">No products found. Try changing filters!</div>
      ) : (
        <>
          <div className="products-grid">
            {products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          
          <Pagination 
            page={page} 
            setPage={setPage} 
            hasMore={products.length === limit} 
          />
        </>
      )}
    </div>
  );
};

export default Products;
