import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, UserPlus, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function Register() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Basic validation
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);

    try {
      await register(formData);
      setSuccess(true);
      // 2 seconds baad automatically login page pe bhej do
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      // Handle validation errors from FastAPI (HTTP 422) or Bad Request (HTTP 400)
      if (err.response?.status === 422) {
        setError('Invalid data format. Please check your inputs.');
      } else {
        setError(err.response?.data?.detail || 'Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f3f4f6', padding: '1rem' }}>
      <div style={{ backgroundColor: 'white', padding: '2.5rem', borderRadius: '1rem', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)', width: '100%', maxWidth: '450px' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#111827', margin: 0 }}>Create Account</h1>
          <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>Join ShopSphere today</p>
        </div>

        {error && (
          <div style={{ backgroundColor: '#fee2e2', color: '#b91c1c', padding: '0.75rem', borderRadius: '0.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem' }}>
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {success && (
          <div style={{ backgroundColor: '#dcfce7', color: '#166534', padding: '0.75rem', borderRadius: '0.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem' }}>
            <CheckCircle2 size={18} />
            Registration successful! Redirecting to login...
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>First Name</label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: '50%', left: '0.75rem', transform: 'translateY(-50%)', color: '#9ca3af' }}>
                  <User size={18} />
                </div>
                <input 
                  type="text" 
                  name="first_name"
                  required 
                  value={formData.first_name}
                  onChange={handleChange}
                  style={{ width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.5rem', outline: 'none', boxSizing: 'border-box' }}
                  placeholder="John"
                />
              </div>
            </div>

            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>Last Name</label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: '50%', left: '0.75rem', transform: 'translateY(-50%)', color: '#9ca3af' }}>
                  <User size={18} />
                </div>
                <input 
                  type="text" 
                  name="last_name"
                  required 
                  value={formData.last_name}
                  onChange={handleChange}
                  style={{ width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.5rem', outline: 'none', boxSizing: 'border-box' }}
                  placeholder="Doe"
                />
              </div>
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>Email Address</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', top: '50%', left: '0.75rem', transform: 'translateY(-50%)', color: '#9ca3af' }}>
                <Mail size={18} />
              </div>
              <input 
                type="email" 
                name="email"
                required 
                value={formData.email}
                onChange={handleChange}
                style={{ width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.5rem', outline: 'none', boxSizing: 'border-box' }}
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>Password</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', top: '50%', left: '0.75rem', transform: 'translateY(-50%)', color: '#9ca3af' }}>
                <Lock size={18} />
              </div>
              <input 
                type="password" 
                name="password"
                required 
                value={formData.password}
                onChange={handleChange}
                style={{ width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.5rem', outline: 'none', boxSizing: 'border-box' }}
                placeholder="Min 8 characters"
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isLoading || success}
            style={{ width: '100%', padding: '0.75rem', backgroundColor: '#4f46e5', color: 'white', border: 'none', borderRadius: '0.5rem', fontWeight: '600', cursor: (isLoading || success) ? 'not-allowed' : 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem', opacity: (isLoading || success) ? 0.7 : 1, marginTop: '0.5rem' }}
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
            {!isLoading && <UserPlus size={18} />}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.875rem', color: '#6b7280' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#4f46e5', textDecoration: 'none', fontWeight: '500' }}>Sign in</Link>
        </p>
      </div>
    </div>
  );
}