import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI } from '../../api/products';
import { Plus, Edit, Trash2 } from 'lucide-react';
import './AdminProducts.css';

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchProducts = async () => {
    try {
      // Admin page par humein saare products chahiye (limit bada di)
      const data = await productsAPI.getProducts({ limit: 100 });
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      // TODO: Connect this to delete API later
      alert(`Deleted product ${id} (UI only for now)`);
    }
  };

  return (
    <div className="admin-page-container">
      <div className="admin-page-header">
        <h1>Products Management</h1>
        <Link to="/admin/products/new" className="admin-btn-primary">
          <Plus size={18} />
          Add New Product
        </Link>
      </div>

      <div className="admin-table-container">
        {loading ? (
          <div className="admin-loading">Loading products...</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.length === 0 ? (
                <tr>
                  <td colSpan="6" className="admin-empty-table">No products found. Add one!</td>
                </tr>
              ) : (
                products.map((p) => (
                  <tr key={p.id}>
                    <td>#{p.id}</td>
                    <td>{p.title}</td>
                    <td>{p.category ? p.category.name : '-'}</td>
                    <td className="price-cell">${p.price.toFixed(2)}</td>
                    <td>
                      <span className={`stock-badge ${p.stock > 0 ? 'stock-in' : 'stock-out'}`}>
                        {p.stock}
                      </span>
                    </td>
                    <td className="actions-cell">
                      <button className="action-btn edit-btn" title="Edit">
                        <Edit size={18} />
                      </button>
                      <button className="action-btn delete-btn" title="Delete" onClick={() => handleDelete(p.id)}>
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default AdminProducts;
