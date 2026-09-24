import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  // Jab tak auth status check ho raha hai, tab tak loading dikhao
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <p style={{ color: '#6b7280', fontSize: '1.125rem' }}>Loading...</p>
      </div>
    );
  }

  // Agar user logged in nahi hai, toh login page par bhej do
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Agar logged in hai, toh protected component render kar do (children)
  return children;
}