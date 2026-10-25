import React, { useState, useEffect } from 'react';
import { api } from '../../api/axios';
import './Dashboard.css';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/dashboard/stats');
        setStats(res.data);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
      }
      setLoading(false);
    };
    fetchStats();
  }, []);

  if (loading) return <div className="admin-dashboard"><p>Loading stats...</p></div>;
  if (!stats) return <div className="admin-dashboard"><p>Stats load nahi hue!</p></div>;

  return (
    <div className="admin-dashboard">
      <h1>Dashboard</h1>
      <p className="dashboard-subtitle">ShopSphere ka aaj ka haal</p>

      {/* ---- STAT CARDS ---- */}
      <div className="stats-grid">
        <div className="stat-card revenue">
          <span className="stat-icon">💰</span>
          <span className="stat-label">Total Revenue</span>
          <span className="stat-value">${stats.revenue.toFixed(2)}</span>
        </div>

        <div className="stat-card orders">
          <span className="stat-icon">📦</span>
          <span className="stat-label">Total Orders</span>
          <span className="stat-value">{stats.total_orders}</span>
        </div>

        <div className="stat-card orders">
          <span className="stat-icon">⏳</span>
          <span className="stat-label">Pending Orders</span>
          <span className="stat-value">{stats.pending_orders}</span>
        </div>

        <div className="stat-card orders">
          <span className="stat-icon">🚚</span>
          <span className="stat-label">Shipped Orders</span>
          <span className="stat-value">{stats.shipped_orders}</span>
        </div>

        <div className="stat-card users">
          <span className="stat-icon">👥</span>
          <span className="stat-label">Total Users</span>
          <span className="stat-value">{stats.total_users}</span>
        </div>

        <div className="stat-card products">
          <span className="stat-icon">🛍️</span>
          <span className="stat-label">Total Products</span>
          <span className="stat-value">{stats.total_products}</span>
        </div>
      </div>

      {/* ---- RECENT ORDERS ---- */}
      <div className="recent-orders-section">
        <h2>Recent Orders</h2>
        <table className="recent-orders-table">
          <thead>
            <tr>
              <th>#ID</th>
              <th>User</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {stats.recent_orders.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '30px', color: '#a0aec0' }}>
                  Abhi tak koi order nahi aaya
                </td>
              </tr>
            ) : (
              stats.recent_orders.map(order => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>User #{order.user_id}</td>
                  <td className="revenue-amount">${order.total_amount.toFixed(2)}</td>
                  <td>
                    <span className={`status-badge status-${order.status}`}>
                      {order.status}
                    </span>
                  </td>
                  <td>{new Date(order.created_at).toLocaleDateString('en-IN')}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminDashboard;
