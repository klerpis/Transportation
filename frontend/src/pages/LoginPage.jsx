import {
  Box, Typography, TextField,
  Button, Paper, Link,
} from '@mui/material';

import { useAuth } from '../contexts/AuthContext';
import { login, getCurrentUser } from "../services/authService";

import { useNavigate, useLocation, } from 'react-router-dom';
// Form, 
import { useState, useEffect } from 'react';
//  useEffect, useCallback


// const Submit = () => {
//   return (
//   <Button variant="contained" color="primary" 
//   fullWidth sx={{ mt: 2 }} type='submit'
//     > Login
//   </Button>
// );};

function LoginForm({ form, handleChange, handleSubmit}){
  return (
        <form onSubmit={handleSubmit}>
          <TextField label="Username" value={form.username} fullWidth
            margin="normal" name='username' onChange={handleChange}/>
          <TextField label="Password" type="password" value={form.password} fullWidth
            margin="normal" name='password' onChange={handleChange} onSubmit={handleSubmit}/>
          {/* < Submit /> */}
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            onClick={handleSubmit}
            >
            Login
            </Button>
        </form>
  )
}



export default function LoginPage() {
    const [form, setForm] = useState({ username: "", password: "" });
    const [logger, setLogger] = useState({error: false, message: ""});
    const navigate = useNavigate();
    const location = useLocation()
    // const { setUser } = useContext(AuthContext);
    const { user, setUser, isLoggedIn, setIsLoggedIn } = useAuth();


    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const navigateToNext = () => {
      console.log('Logged in:', location, typeof location.search, isLoggedIn, !user, !!user);
      let to_address = location.search?.split('?')[1]?.split('=')[1]?.split('/') || ['', ''];
      console.log("to_address 1", to_address)
      to_address = to_address.join('/');
      
      console.log("to_address 2", to_address)
      if (to_address){
        try {navigate('/'+to_address);} 
        catch {navigate('/profile');}
      } else {
        navigate('/profile');
      };

    }

    const handleSubmit = async (e) => {
      e.preventDefault();
      const log = await login(form);
      if (!log.success){
        setForm({ username:"", password: "" })
        setLogger({error: !log.success, message: log.message})
        return
      }
      
      const data = await getCurrentUser();
      setUser((prevData) => {
        try {
          // localStorage.setItem("access", data.access);
          localStorage.setItem("user_name", data.username);
          localStorage.setItem("user_email", data.email);
          
          console.log('Successfully set the items', localStorage.getItem("access"));
        } catch (e) {
          console.log('could not set item', e)
        }
        return data

      });
      setIsLoggedIn(true);
      
      // localStorage.setItem("user_email", credentials.email);
      // You can also store user_id, name, etc.
      
      // navigate("/");
      navigateToNext()
    };

      useEffect(() => {
        if (!(localStorage.getItem("access"))) {
          // axios localstorage set access to null if refresh error reaches
            console.log('localStorage.getItem("access")', localStorage.getItem("access"), isLoggedIn)
            // setIsLoggedIn(false)
          }
          else {navigateToNext();} // if already logged in and the user just types in /login manually

          
          }, [])


  return (
    <Box display="flex" justifyContent="center" mt={5}>

      <Paper elevation={4} sx={{ p: 4, width: '100%', maxWidth: 400 }}>
      {logger.error && (
        <Typography variant="h6" textAlign='center' color='error' gutterBottom>
          {logger.message}
        </Typography>
        )}
        <Typography variant="h5" gutterBottom>
          Login to Your Account
        </Typography>

        <LoginForm form={form} handleChange={handleChange} handleSubmit={handleSubmit} />

        <Typography variant="body2" sx={{ mt: 2 }}>
          Don't have an account?{' '}
          <Link href="/register" underline="hover">
            Register here
          </Link>
        </Typography>
      </Paper>
    </Box>
  );
}
