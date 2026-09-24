import React, { useState, useEffect } from 'react';
import { categoriesAPI } from '../../api/products';
import { Plus, Edit, Trash2, FolderTree } from 'lucide-react';
import './AdminCategories.css'; // Halka sa naya CSS use karenge

const AdminCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Nayi category form ke liye state
  const [showForm, setShowForm] = useState(false);
  const [newCat, setNewCat] = useState({ name: '', description: '' });
  const [saving, setSaving] = useState(false);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const data = await categoriesAPI.getCategories();
      setCategories(data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleAddCategory = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await categoriesAPI.createCategory(newCat);
      setNewCat({ name: '', description: '' });
      setShowForm(false);
      // Nayi aane ke baad list ko refresh karlo
      fetchCategories();
    } catch (error) {
      console.error("Error creating category:", error);
      alert("Category banne me error aayi.");
    }
    setSaving(false);
  };

  return (
    <div className="admin-page-container">
      <div className="admin-page-header">
        <h1>Categories</h1>
        <button className="admin-btn-primary" onClick={() => setShowForm(!showForm)}>
          <Plus size={18} />
          Add Category
        </button>
      </div>

      {showForm && (
        <div className="form-card category-form-card">
          <h3>Create New Category</h3>
          <form onSubmit={handleAddCategory} className="admin-form">
            <div className="form-group">
              <label>Name</label>
              <input 
                type="text" 
                value={newCat.name}
                onChange={(e) => setNewCat({ ...newCat, name: e.target.value })}
                placeholder="e.g. Footwear"
                required 
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea 
                value={newCat.description}
                onChange={(e) => setNewCat({ ...newCat, description: e.target.value })}
                placeholder="Short description..."
                rows="2"
              />
            </div>
            <button type="submit" className="admin-btn-primary submit-btn" disabled={saving}>
              {saving ? "Saving..." : "Save Category"}
            </button>
          </form>
        </div>
      )}

      <div className="admin-table-container">
        {loading ? (
          <div className="admin-loading">Loading categories...</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Category Name</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.length === 0 ? (
                <tr>
                  <td colSpan="4" className="admin-empty-table">No categories yet.</td>
                </tr>
              ) : (
                categories.map((c) => (
                  <tr key={c.id}>
                    <td>#{c.id}</td>
                    <td style={{ fontWeight: '600', color: '#4fd1c5' }}>
                      <FolderTree size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} />
                      {c.name}
                    </td>
                    <td>{c.description || '-'}</td>
                    <td className="actions-cell">
                      <button className="action-btn edit-btn" title="Edit">
                        <Edit size={18} />
                      </button>
                      <button className="action-btn delete-btn" title="Delete">
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

export default AdminCategories;
