
import { Card, CardContent,
  Typography, Box, Tooltip, Chip, Button, Stack } from '@mui/material'; 
  
import dayjs from 'dayjs';



 function renderFeedbackChip(booking, onFeedbackClick) {
  const now = dayjs();
  const deadline = dayjs(booking.feedback_deadline);

    if (booking.status === 'completed' && !booking.feedback_submitted) {
      if (now.isBefore(deadline)) {
        return (
          <Tooltip title="Click to leave a feedback (24hr limit)">
            <Chip
              label="Feedback"
              color="warning"
              clickable
              onClick={() => onFeedbackClick(booking)}
            />
          </Tooltip>
        );
      } else {
        return (
          <Tooltip title="Feedback time expired (36hr limit)">
            <Chip label="Expired" color="default" clickable />
          </Tooltip>
          )
      }
    }
    

    if (booking.feedback_submitted && !booking.feedback_resolved) {
      return (
          <Tooltip title="Feedback already submitted">
            <Chip label="Submitted" color="info" clickable />
          </Tooltip>
          )
          
        }
      else if (booking.feedback_submitted && booking.feedback_resolved) {
        return (
          <Tooltip title="Feedback already submitted">
            <Chip label="Resolved" color="info" clickable />
          </Tooltip>
          )

      }

    if (booking.status === 'cancelled') {
      return (
          <Tooltip title="no need for feedback">
            <Chip label="Review Closed" color="default" clickable />
          </Tooltip>
          ) 
        }

    if (booking.status === 'confirmed') {
      return (
          <Tooltip title="Opened after trip">
            <Chip label="Locked" color="default" clickable />
          </Tooltip>
          ) 
        }
        

    return <Tooltip title="Confirmation status pending">
            <Chip label="Locked" color="default" clickable />
          </Tooltip> 
}


export default function BookingCard({ booking, onCancel, onTrack, handleOpenFeedbackModal }) {
  const { id, isUpcoming } = booking; 
  return (
      <Card elevation={3}>
        <CardContent>
          <Typography variant="h6">
            {booking.from_location} → {booking.to_location}
          </Typography>
          <Typography color="text.secondary">
            {booking.from_street} → {booking.to_street}
          </Typography>

          <Typography sx={{ mt: 1 }} gutterBottom>
            {booking.departure_date} at {booking.departure_time}
          </Typography>

          <Typography variant="body2">Booking ID: {booking.booking_id}</Typography>

          <Box sx={{ mt: 1, mb: 2 }}>
            <Chip
              label={booking.status}
              color={booking.status === 'confirmed' ? 'success' : booking.status === 'completed' ? 'default' : 'error'}
              clickable
              sx={{ mr: 1 }}
            />
            {renderFeedbackChip(booking, handleOpenFeedbackModal)}
          </Box>

          <Stack direction="row" spacing={2}>
            {isUpcoming && (
              <>
                <Button variant="outlined" color="error" onClick={() => onCancel(id)}>
                  Cancel
                </Button>
                <Button variant="contained" color="primary" onClick={() => onTrack(id)}>
                  Track
                </Button>
              </>
            )}
          </Stack>
        </CardContent>
      </Card>

  );
}






    // <Card elevation={3}>
    //   <CardContent>
    //     <Typography variant="h6">
    //       {from_location} → {to_location}
    //     </Typography>
    //     <Typography color="text.secondary" gutterBottom>
    //       {departure_date} at {departure_time}
    //     </Typography>
    //     <Typography variant="body2">Booking ID: {id}</Typography>

    //     <Box sx={{ mt: 1, mb: 2 }}>
    //       <Chip 
    //         label={status}
    //         color={status === 'confirmed' ? 'success' : status === 'completed' ? 'default': 'error'}
    //         clickable={true}
    //         sx={{ mr: 1 }}

    //       />
    //       {renderFeedbackChip(booking, handleOpenFeedbackModal)}
    //     </Box>

    //     <Stack direction="row" spacing={2}>
    //       {isUpcoming && (
    //         <>
    //           <Button variant="outlined" color="error" onClick={() => onCancel(id)}>
    //             Cancel
    //           </Button>
    //           <Button variant="contained" color="primary" onClick={() => onTrack(id)}>
    //             Track
    //           </Button>
    //         </>
    //       )}
    //     </Stack>
    //   </CardContent>
    // </Card>



  
  
  
  
  
  
  
  
  
  
  
  
  