import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShoppingBag, User, LogOut } from 'lucide-react';

export default function MainLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Navbar */}
      <nav style={{ backgroundColor: 'rgba(15, 23, 42, 0.8)', backdropFilter: 'blur(10px)', borderBottom: '1px solid rgba(255,255,255,0.1)', position: 'sticky', top: 0, zIndex: 10 }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '4rem' }}>
            
            {/* Logo */}
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none', color: '#4fd1c5', fontWeight: 'bold', fontSize: '1.25rem' }}>
              <ShoppingBag size={24} />
              <span>ShopSphere</span>
            </Link>

            {/* Right Side Nav */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              {user ? (
                // Agar user logged in hai:
                <>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#e2e8f0', fontSize: '0.875rem', fontWeight: '500', marginRight: '1rem' }}>
                    <User size={18} />
                    <span>Hi, {user.first_name || 'User'}</span>
                  </div>
                  
                  <button 
                    onClick={handleLogout}
                    style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', backgroundColor: '#fee2e2', color: '#b91c1c', border: 'none', padding: '0.5rem 0.75rem', borderRadius: '0.375rem', fontSize: '0.875rem', fontWeight: '500', cursor: 'pointer' }}
                  >
                    <LogOut size={16} />
                    Logout
                  </button>
                </>
              ) : (
                // Agar user logged out hai:
                <>
                  <Link to="/login" style={{ color: '#4fd1c5', textDecoration: 'none', fontWeight: '500', fontSize: '0.875rem' }}>
                    Log in
                  </Link>
                  <Link to="/register" style={{ backgroundColor: '#4fd1c5', color: '#0f172a', textDecoration: 'none', padding: '0.5rem 1rem', borderRadius: '0.375rem', fontWeight: '600', fontSize: '0.875rem' }}>
                    Sign up
                  </Link>
                </>
              )}
            </div>

          </div>
        </div>
      </nav>

      {/* Main Content (Jahan pages render honge) */}
      <main style={{ flex: 1, padding: '2rem 1.5rem', maxWidth: '1200px', margin: '0 auto', width: '100%', boxSizing: 'border-box' }}>
        <Outlet />
      </main>

    </div>
  );
}