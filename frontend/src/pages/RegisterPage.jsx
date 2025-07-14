import { useState } from "react";
import {
  Box, Button, Paper, TextField, Typography, Snackbar, Alert, Link
} from "@mui/material";
import { register } from "../services/authService";
import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const navigate = useNavigate();

  const originalData = { username: '', email: '', password: '', password2: '' };
  const [form, setForm] = useState(originalData);
  const [errors, setErrors] = useState({});
  const [snackbar, setSnackbar] = useState({ open: false, message: "", type: "success" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: null }); // clear field error as user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    try {
      const res = await register(form);
      setSnackbar({ open: true, message: "✅ Registration successful!", type: "success" });
      setTimeout(() => navigate("/login"), 1000);
    } catch (err) {
      const data = err.response?.data;

      if (data) {
        setErrors(data); // Field-level errors
        setSnackbar({
          open: true,
          message: data.detail || "❌ Registration failed. Please correct the errors.",
          type: "error"
        });
      }
    }
  };

  return (
    <Box display="flex" justifyContent="center" mt={5}>
      <Paper elevation={4} sx={{ p: 4, width: '100%', maxWidth: 400 }}>
        <Typography variant="h5" gutterBottom>
          Create an Account
        </Typography>

        <form onSubmit={handleSubmit}>
          <TextField
            label="Full Name"
            name="username"
            fullWidth margin="normal"
            value={form.username}
            onChange={handleChange}
            error={!!errors.username}
            helperText={errors.username?.[0]}
          />
          <TextField
            label="Email"
            name="email"
            fullWidth margin="normal"
            value={form.email}
            onChange={handleChange}
            error={!!errors.email}
            helperText={errors.email?.[0]}
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            fullWidth margin="normal"
            value={form.password}
            onChange={handleChange}
            error={!!errors.password}
            helperText={errors.password?.[0]}
          />
          <TextField
            label="Password (again)"
            name="password2"
            type="password"
            fullWidth margin="normal"
            value={form.password2}
            onChange={handleChange}
            error={!!errors.password2}
            helperText={errors.password2?.[0]}
          />

          {errors.non_field_errors && (
            <Typography variant="body2" color="error" sx={{ mt: 1, ml: 3 }}>
              {errors.non_field_errors[0]}
            </Typography>
          )}

          <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>
            Register
          </Button>
        </form>

        <Typography variant="body2" sx={{ mt: 2 }}>
          Already have an account?{" "}
          <Link href="/login" underline="hover">
            Login here
          </Link>
        </Typography>
      </Paper>

      {/* ✅ Snackbar for success/failure */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.type}
          variant="filled"
          sx={{ fontWeight: 600 }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
