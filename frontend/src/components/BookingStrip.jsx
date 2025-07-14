import { Grid, TextField, Button } from '@mui/material';

import { useNavigate } from 'react-router-dom';
import { useState } from "react";

const HomePageBookingStrip = ()=> {
    const [bookingForm, setBookingForm] = useState({
        departure: "",
        destination: "",
        date: '',
    });
    const navigate = useNavigate();
    const handleChange = (e) => {
        setBookingForm(prev => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
        // console.log("Booking", bookingForm)
        // alert(bookingForm)
        navigate('/book')
    };

    return (
        <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                <TextField
                    label="Departure"
                    name="departure"
                    type="time"
                    value={bookingForm.departure}
                    onChange={handleChange}
                    fullWidth
                />
                </Grid>
                <Grid item xs={12} md={4}>
                <TextField
                    label="Destination"
                    name="destination"
                    value={bookingForm.destination}
                    onChange={handleChange}
                    fullWidth
                />
                </Grid>
                <Grid item xs={12} md={3}>
                <TextField
                    label="Date"
                    type="date"
                    name="date"
                    value={bookingForm.date}
                    onChange={handleChange}
                    InputLabelProps={{ shrink: true }}
                    fullWidth
                />
                </Grid>
                <Grid item xs={12} md={1}>
                <Button type="submit" variant="contained" fullWidth
                    onClick={()=> navigate('/book')}
                >
                    Go
                </Button>
                </Grid>
            </Grid>
        </form>
  );
};


export { HomePageBookingStrip };