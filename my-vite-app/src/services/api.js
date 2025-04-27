// src/services/api.js
import axios from 'axios';

const API_URL = "http://127.0.0.1:8000";  // Update with your FastAPI backend URL

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor to attach the JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
      config.headers["Authorization"] = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
