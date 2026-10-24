import React, { useState, useEffect } from 'react';
import { checkoutAPI } from '../../api/checkout';
import './Orders.css';

const STATUS_OPTIONS = ['PENDING', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED'];

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const data = await checkoutAPI.getAllOrders();
      setOrders(data);
    } catch (err) {
      console.error("Orders fetch error:", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      await checkoutAPI.updateOrderStatus(orderId, newStatus);
      // Local state update karo (re-fetch se bhi ho sakta tha, but ye faster hai)
      setOrders(prev =>
        prev.map(o => o.id === orderId ? { ...o, status: newStatus } : o)
      );
    } catch (err) {
      console.error("Status update error:", err);
    }
  };

  if (loading) return <div className="admin-orders-page"><p>Loading orders...</p></div>;

  return (
    <div className="admin-orders-page">
      <h1>All Orders ({orders.length})</h1>

      {orders.length === 0 ? (
        <div className="no-orders">Abhi tak koi order nahi aaya!</div>
      ) : (
        <div className="orders-table-wrapper">
          <table className="orders-table">
            <thead>
              <tr>
                <th>#ID</th>
                <th>Customer</th>
                <th>Items</th>
                <th>Amount</th>
                <th>Date</th>
                <th>Status</th>
                <th>Update Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>#{order.id}</td>

                  <td>User #{order.user_id}</td>

                  <td>
                    <div className="order-items-list">
                      {order.items.map(item => (
                        <div key={item.id}>
                          {item.product ? item.product.title : 'Product deleted'} ×{item.quantity}
                        </div>
                      ))}
                    </div>
                  </td>

                  <td className="order-amount">
                    ${order.total_amount.toFixed(2)}
                  </td>

                  <td>
                    {new Date(order.created_at).toLocaleDateString('en-IN')}
                  </td>

                  <td>
                    <span className={`status-badge status-${order.status}`}>
                      {order.status}
                    </span>
                  </td>

                  <td>
                    <select
                      className="status-select"
                      value={order.status}
                      onChange={(e) => handleStatusChange(order.id, e.target.value)}
                    >
                      {STATUS_OPTIONS.map(s => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminOrders;
