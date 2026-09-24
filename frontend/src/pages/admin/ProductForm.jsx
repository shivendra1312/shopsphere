import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../../api/products';
import { ArrowLeft, Save } from 'lucide-react';
import './ProductForm.css';

const ProductForm = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    stock: '',
    category_id: ''
  });

  useEffect(() => {
    // Categories layenge taaki dropdown me dikha sakein
    const fetchCategories = async () => {
      try {
        const data = await categoriesAPI.getCategories();
        setCategories(data);
      } catch (err) {
        console.error("Categories fetch error", err);
      }
    };
    fetchCategories();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // API call: Naya product create karo
      await productsAPI.createProduct({
        title: formData.title,
        description: formData.description,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock),
        category_id: parseInt(formData.category_id)
      });
      
      // Success pe wapas products table pe bhej do
      navigate('/admin/products');
    } catch (err) {
      setError("Product create karne me error aayi. Please check data.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="admin-form-container">
      <div className="admin-page-header">
        <h1>Add New Product</h1>
        <button onClick={() => navigate('/admin/products')} className="admin-btn-secondary">
          <ArrowLeft size={18} />
          Back to List
        </button>
      </div>

      <div className="form-card">
        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="admin-form">
          <div className="form-group">
            <label>Product Title</label>
            <input 
              type="text" 
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g. Nike Air Max"
              required 
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea 
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Detailed description of the product..."
              rows="4"
              required 
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Price ($)</label>
              <input 
                type="number" 
                name="price"
                step="0.01"
                min="0"
                value={formData.price}
                onChange={handleChange}
                placeholder="0.00"
                required 
              />
            </div>
            
            <div className="form-group">
              <label>Stock (Quantity)</label>
              <input 
                type="number" 
                name="stock"
                min="0"
                value={formData.stock}
                onChange={handleChange}
                placeholder="100"
                required 
              />
            </div>
          </div>

          <div className="form-group">
            <label>Category</label>
            <select 
              name="category_id"
              value={formData.category_id}
              onChange={handleChange}
              required
            >
              <option value="" disabled>Select a category</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <button type="submit" className="admin-btn-primary submit-btn" disabled={loading}>
            <Save size={18} />
            {loading ? "Saving..." : "Save Product"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProductForm;
