import { api } from './axios';

export const authAPI = {
  // 1. Register a new user
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // 2. Login
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    // JWT tokens ko local storage me save kar rahe hain
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }
    return response.data;
  },

  // 3. Logout
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      } catch (error) {
        console.error("Logout error", error);
      }
    }
    // Local storage clear karna zaroori hai
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // 4. Get Current User Profile (ye apne aap auth token bhejega interceptor ke through)
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};