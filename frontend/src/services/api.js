// frontend/src/services/api.js
import axios from "axios";
import { tokenManager } from "../utils/tokenManager";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    const token = tokenManager.getAccessToken();

    if (token && !tokenManager.isTokenExpired()) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (tokenManager.getRefreshToken()) {
      // Try to refresh token
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: tokenManager.getRefreshToken(),
        });

        const { access_token } = response.data;
        tokenManager.setTokens(access_token, tokenManager.getRefreshToken());
        config.headers.Authorization = `Bearer ${access_token}`;
      } catch (error) {
        // Refresh failed, redirect to login
        tokenManager.clearTokens();
        window.location.href = "/login";
        return Promise.reject(error);
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenManager.clearTokens();
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post("/auth/login", credentials),
  register: (userData) => api.post("/auth/register", userData),
  refresh: (refreshToken) =>
    api.post("/auth/refresh", { refresh_token: refreshToken }),
  me: () => api.get("/auth/me"),
};

export default api;
