import axios from "axios";

const baseURL = "http://localhost:8000/api"; // adjust for production

const instance = axios.create({
  baseURL,
});

// Automatically attach token to headers
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  const publicRoutes = ["/login/", "/register/", "/auth/token/refresh/"];
  const isPublic = publicRoutes.some(route => config.url.includes(route));

  if (token && !isPublic) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
  },
  (error) => Promise.reject(error)
);


// Add interceptor for auto-refresh
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Handle 401 due to expired access token
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem("refresh")
    ) {
      originalRequest._retry = true;
      try {
        const res = await axios.post("/auth/token/refresh/", {
          refresh: localStorage.getItem("refresh"),
        });

        const newAccess = res.data.access;
        localStorage.setItem("access", newAccess);
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return instance(originalRequest); // Retry request
      } catch (refreshError) {
        // Refresh failed → redirect to login
        // localStorage.clear();
        
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default instance;
