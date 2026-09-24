import React from 'react';
import { NavLink, Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Package, FolderTree, LogOut, ArrowLeft } from 'lucide-react';
import './AdminLayout.css';

const AdminLayout = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="admin-layout">
      {/* 1. Left Sidebar */}
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">
          <LayoutDashboard size={24} />
          Admin Panel
        </Link>
        
        <nav className="admin-nav">
          {/* NavLink automatically active class add karta hai */}
          <NavLink to="/admin/products" className={({ isActive }) => isActive ? "admin-nav-link active" : "admin-nav-link"}>
            <Package size={20} />
            Products
          </NavLink>
          
          <NavLink to="/admin/categories" className={({ isActive }) => isActive ? "admin-nav-link active" : "admin-nav-link"}>
            <FolderTree size={20} />
            Categories
          </NavLink>

          <Link to="/" className="admin-nav-link" style={{ marginTop: '20px' }}>
            <ArrowLeft size={20} />
            Back to Shop
          </Link>
        </nav>

        <button onClick={handleLogout} className="admin-logout-btn">
          <LogOut size={18} style={{ display: 'inline', marginRight: '8px' }} />
          Log Out
        </button>
      </aside>

      {/* 2. Main Content Area */}
      <main className="admin-main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default AdminLayout;
