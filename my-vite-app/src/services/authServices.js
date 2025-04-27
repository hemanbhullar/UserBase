import apiClient from './api';  // Import the Axios instance

export const login = async (username, password) => {
  const response = await apiClient.post("/login/", { username, password });
  if (response.data.access_token) {
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("refresh_token", response.data.refresh_token);
  }
  return response.data;
};

export const register = async (username, email, password, role) => {
  const response = await apiClient.post("/register/", {
    username,
    email,
    password,
    role,
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await apiClient.get("/me/");
  return response.data;
};
