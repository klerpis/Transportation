import { useEffect, useState } from "react";
import {
  Box, Typography, TextField, Rating, Button, Divider, Paper
} from "@mui/material";
import axios from "../api/axios";
import ReviewCarousel from "../components/ReviewCarousel";

// import "slick-carousel/slick/slick.css";
// import "slick-carousel/slick/slick-theme.css";



export default function ReviewsPage() {
  const [review, setReview] = useState({ name: '', email: '', rating: 0, comment: '' });
  const [allReviews, setAllReviews] = useState([]);
  const [loading, setLoading] = useState(false);


//   const allReviews = [
//   {
//     name: 'Chidera',
//     rating: 5,
//     comment: 'Fantastic experience! Easy booking.',
//   },
//   {
//     name: 'Obinna',
//     rating: 4,
//     comment: 'Timely service and clean vehicles.',
//   },
// ];

  
  // Fetch existing reviews
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await axios.get("/reviews/");
        setAllReviews(res.data);
        console.log("REVIEWS", res.data)
      } catch (err) {

        // alert("Failed to load reviews.");
      }
    };
    fetchReviews();
  }, []);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const payload = { ...review, rating: review.rating || 5 };
      await axios.post("/reviews/create/", payload);
      alert("✅ Review submitted!");
      setReview({ name: '', email: '', rating: 0, comment: '' });
      // const res = await axios.get("/reviews/");
      // setAllReviews(res.data);
    } catch (e) {
      alert("❌ Failed to submit review.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, mx: "auto" }}>
      <Typography variant="h4" gutterBottom>Leave a Review</Typography>

      <TextField
        label="Your Name" fullWidth sx={{ mb: 2 }}
        value={review.name}
        onChange={(e) => setReview({ ...review, name: e.target.value })}
      />
      <TextField
        label="Your Email (optional)" fullWidth sx={{ mb: 2 }}
        value={review.email}
        onChange={(e) => setReview({ ...review, email: e.target.value })}
      />
      <Rating
        value={review.rating}
        onChange={(e, newValue) =>
          setReview({ ...review, rating: newValue })
        }
      />
      <TextField
        label="Your Review" fullWidth multiline rows={4}
        sx={{ my: 2 }} value={review.comment}
        onChange={(e) => setReview({ ...review, comment: e.target.value })}
      />
      <Button variant="contained" onClick={handleSubmit} disabled={loading}>
        {loading ? "Submitting..." : "Submit Review"}
      </Button>

      <Divider sx={{ my: 4 }} />
        <Typography variant="h5" gutterBottom>What Others Are Saying {allReviews.length} </Typography>
        <ReviewCarousel reviews={allReviews} />
          
    </Box>
  );
}
