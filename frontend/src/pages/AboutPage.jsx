import { Box, Typography, Grid, Paper, 
  Avatar, Rating } from '@mui/material';
import { useState, useEffect } from 'react';
import axios from '../api/axios';

import ContactSupport from '../components/ContactSupport';

const testimonials = [
  {
    name: 'Ada',
    review: 'Smooth booking, arrived on time. Will use again!',
    rating: 5,
  },
  {
    name: 'Tunde',
    review: 'Clean bus, helpful driver. 10/10.',
    rating: 4,
  },
];

export default function AboutPage() {
  const [reviews, setReviews] = useState([])
  useEffect(() => {

      async function getReviews() {
          try {
              const res = await axios.get("/reviews/");
              setReviews(res.data)
              // alert("✅ Feedback submitted!");
              // onClose();
              // refreshBookings(); // optional refetch to update UI
          } catch (e) {
              console.log('reviews delayed')
              // alert(e.response?.data?.error || "❌ Could not submit feedback");
          }
      } 
  getReviews()
  }, [])

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        About Us
      </Typography>
      <Typography variant="body1" paragraph>
        We are committed to making road travel across Nigeria smarter, faster, and safer.
        Whether you're booking a trip from Lagos to Abuja or tracking your live journey, our platform is designed for reliability and comfort.
      </Typography>

      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        What Our Customers Say
      </Typography>
      <Grid container spacing={3}>
        {reviews.map((t, i) => (
        // {testimonials.map((t, index) => (
          <Grid item xs={12} md={6} key={i}>
            <Paper sx={{ p: 3 }}>
              <Grid container spacing={2}>
                <Grid item>
                  <Avatar>{t.name[0]}</Avatar>
                </Grid>
                <Grid item xs>
                  <Typography variant="subtitle1">{t.name}</Typography>
                  <Rating value={t.rating} readOnly />
                  <Typography variant="body2" color="text.secondary">
                    {t.comment}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        ))}
      </Grid>
      
      <ContactSupport />

    </Box>
  );
};
