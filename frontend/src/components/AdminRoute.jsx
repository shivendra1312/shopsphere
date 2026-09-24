import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminRoute = ({ children }) => {
  const { user } = useAuth();

  // 1. Agar user login nahi hai, toh login page pe bhejo
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // 2. Agar user login hai, par ADMIN nahi hai, toh home page pe bhej do
  if (user.role !== 'admin' && user.role !== 'ADMIN') {
    return <Navigate to="/" replace />;
  }

  // 3. Agar admin hai, toh component render karo
  return children;
};

export default AdminRoute;
