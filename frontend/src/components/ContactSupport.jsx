import { Typography, TextField, Button, 
            Grid, Box, Stack
        } from '@mui/material';
import { useState } from "react";
import axios from "../api/axios";

export default function ContactSupport({sx}){
    const [form, setForm] = useState({
        name: "", email: "", subject: "", message: ""
    });
    const [loading, setLoading] = useState(false);

     const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
        await axios.post("/support/create/", form);
        alert("✅ Message submitted successfully!");
        setForm({ name: "", email: "", subject: "", message: "" });
        } catch (e) {
        alert("❌ Submission failed.");
        } finally {
        setLoading(false);
        }
    };


    return (
        // {...sx}
        <Box sx={{ mt: 6 }} {...sx} > 
            <Typography variant="h5" sx={{alignItems: 'left'}} gutterBottom>Contact Support</Typography>
            <Typography variant="body2" gutterBottom>
                Have a complaint or question? Let us know.
            </Typography>

            <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                    <TextField fullWidth name="name" 
                    label="Name" value={form.name} onChange={handleChange} color="warning" sx={{mb:1}}  />
                    <TextField fullWidth name="email" 
                    label="Email Address" value={form.email} onChange={handleChange} color="warning" sx={{mb:1}} />
                    <TextField fullWidth name="subject" 
                    label="Subject" value={form.subject} onChange={handleChange} color="warning" sx={{mb:1}} />
                    <TextField fullWidth name="message" 
                    label="Message" value={form.message} onChange={handleChange} color="warning" sx={{mb:1}} multiline rows={4}/>
                </Grid>
                <Button variant="contained" color="warning"
                onClick={handleSubmit} disabled={loading}
                >{loading ? "Sending..." : "Submit"}</Button>
                <Grid item xs={12}>
                </Grid>
            </Grid>

            {/* <Stack spacing={2}>
                <TextField name="name" label="Your Name" value={form.name} onChange={handleChange} fullWidth />
                <TextField name="email" label="Email Address" value={form.email} onChange={handleChange} fullWidth />
                <TextField name="subject" label="Subject" value={form.subject} onChange={handleChange} fullWidth />
                <TextField name="message" label="Message" value={form.message} onChange={handleChange} multiline rows={4} fullWidth />
                <Button variant="contained" onClick={handleSubmit} disabled={loading}>
                {loading ? "Sending..." : "Submit"}
                </Button>
            </Stack> */}
            
        </Box>

    )
}

