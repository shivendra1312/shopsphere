import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';
import AdminLayout from './layouts/AdminLayout';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Home from './pages/Home';
import AdminProducts from './pages/admin/Products';
import ProductForm from './pages/admin/ProductForm';
import AdminCategories from './pages/admin/Categories';

// Ek simple placeholder Profile page testing ke liye
function Profile() {
  return (
    <div>
      <h2>Your Secure Profile Page</h2>
      <p>Only logged in users can see this!</p>
    </div>
  );
}

function App() {
  return (
    // 1. BrowserRouter navigation ke liye
    <BrowserRouter>
      {/* 2. AuthProvider poore app ko user state dega */}
      <AuthProvider>
        
        {/* 3. Routes define karte hain */}
        <Routes>
          {/* MainLayout ke andar saare public pages aayenge */}
          <Route element={<MainLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:id" element={<ProductDetail />} />
          </Route>

          {/* AdminLayout ke andar saare Admin pages aayenge */}
          <Route 
            path="/admin" 
            element={
              <AdminRoute>
                <AdminLayout />
              </AdminRoute>
            }
          >
            {/* Jab koi sirf /admin pe aayega, usko products dikhayenge */}
            <Route index element={<AdminProducts />} />
            <Route path="products" element={<AdminProducts />} />
            <Route path="products/new" element={<ProductForm />} />
            <Route path="categories" element={<AdminCategories />} />
          </Route>

        </Routes>

      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;