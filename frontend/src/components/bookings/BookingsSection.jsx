import { Typography, Grid } from '@mui/material';
import BookingCard from './BookingCard';




export default function BookingsSection({ title, bookings, onCancel, onTrack, handleOpenFeedbackModal }) {
  return (
    <>
      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        {title}
      </Typography>
      <Grid container spacing={2}>
        {bookings.length === 0 ? (
          <Typography color="text.secondary">No bookings yet.</Typography>
        ) : (
          bookings.map((b) => (
            <Grid item xs={12} md={6} key={b.id}>
              <BookingCard booking={b} onCancel={onCancel} onTrack={onTrack} 
                           handleOpenFeedbackModal={handleOpenFeedbackModal}/>
            </Grid>
          ))
        )}
      </Grid>
    </>
  );
}












