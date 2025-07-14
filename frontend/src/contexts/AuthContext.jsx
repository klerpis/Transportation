import { createContext, useContext, useState } from 'react';
import { getCurrentUser, logout } from "../services/authService";
import { useEffect } from 'react';


const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // replace with real auth later
  const [isLoggedIn, setIsLoggedIn] = useState(false); // replace with real auth later


  
  const fetchUser = async () => {
    try {
          const data = await getCurrentUser();
          setUser(data);
        } catch {
          setUser(null);
        }};

    const checkLogged = ()=> {
        // const data = await getCurrentUser();
        const token = localStorage.getItem("access");
        const email = localStorage.getItem("user_email");
        const username = localStorage.getItem("user_name");
        
        if (token && email && username) {
          // setIsLoggedIn((prev)=> true)
          setUser({username, email, token})
          console.log("GOT the token, email and username ", token, email, username)
          // setAuth({ token, email, username }); // or however your auth state is structured
          setIsLoggedIn(true)
          return true
        } else {
          // setIsLoggedIn((prev)=> false)
          // setUser(null);
          console.log("could not get token, email and username ", token, email, username)
          return false
        }
      
}

  useEffect(() => {
    if (checkLogged()) {
      fetchUser();
    }
  }, []);


  const handleLogout = () => {
    logout();
    setUser(null);
    setIsLoggedIn(false)
  };

  return (
    <AuthContext.Provider value={{ user, isLoggedIn, setIsLoggedIn, setUser, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
