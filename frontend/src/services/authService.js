import axios from "../api/axios";


export const login = async (credentials) => {
  try {
    const res = await axios.post("/auth/token/", credentials);
    console.log('res', res)
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);

    return { success: true };
  } catch (error) {
    if (error.response && error.response.status === 401) {
      return { success: false, message: "Invalid username or password" };
    } else {
      return { success: false, message: "Something went wrong. Please try again." };
    }
  }
};

export const register = async (data) => {
    const res = await axios.post("/register/", data);
  return res.data
  };

export const getCurrentUser = async () => {
  const res = await axios.get("/me/");
  // const res = {data:{}}
  
  return res.data;
};

export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
