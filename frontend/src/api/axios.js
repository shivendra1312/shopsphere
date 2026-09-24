import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Ek custom axios instance banaya
export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// REQUEST INTERCEPTOR: Har request jaane se pehle local storage se token utha ke headers me daal dega
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// RESPONSE INTERCEPTOR: Agar 401 (Unauthorized) error aaye, toh refresh token use karke naya access token layega
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Agar error 401 hai aur ye retry nahi ho rahi hai
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          // Naya access token mangwao
          const response = await axios.post(`${BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          // Naye tokens local storage me save karo
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);

          // Purani failed request ko naye token ke sath dobara bhejo
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Agar refresh bhi fail ho jaye toh user ko logout kar do
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);