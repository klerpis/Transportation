
import { Dialog, DialogTitle,
    DialogContent, DialogActions, Button, TextField, Rating, Box,
} from '@mui/material';

import axios from '../../api/axios';

import { useState } from 'react';


export default function FeedbackDialog({ open, onClose, onSubmit, booking }) {
  const [rating, setRating] = useState(0);
  // const [text, setText] = useState('');
  const [feedbackText, setFeedbackText] = useState('');

  // const handleSubmit = () => {
  //   onSubmit({ bookingId: booking.id, rating, text });
  //   onClose();
  // };
  const handleSubmitFeedback = async () => {
    try {
      const res = await axios.post("/feedbacks/create/", {
        booking: booking.id,
        feedback_text: feedbackText,
        rating: rating,
      });
      alert("✅ Feedback submitted!");
      onClose();
      // refreshBookings(); // optional refetch to update UI
    } catch (e) {
      alert(e.response?.data?.error || "❌ Could not submit feedback");
    }
};


  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Feedback for {booking.from} → {booking.to}</DialogTitle>
      <DialogContent>
        <Box sx={{ my: 2 }}>
          <Rating
            value={rating}
            onChange={(e, newValue) => setRating(newValue)}
          />
        </Box>
        <TextField
          label="Your Feedback"
          fullWidth
          multiline
          rows={4}
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmitFeedback} disabled={!rating || !feedbackText}>
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
}
