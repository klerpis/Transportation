// BookingsPage.jsx
import React, { useEffect, useState } from "react";
import {
  Box, Typography, Stack, Card, CardContent,
  TextField, Modal, Button, CircularProgress, Grid, Divider, ToggleButtonGroup, ToggleButton
} from "@mui/material";
import MapView from "../components/map/MapView";
import FeedbackDialog from "../components/feedback/FeedbackDialog";

import BookingCard from '../components/bookings/BookingCard';
import axios from "../api/axios";


export default function BookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [viewStyle, setViewStyle] = useState('compact');

  const [feedbackModalOpen, setFeedbackModalOpen] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState(null);
  const [mapOpen, setMapOpen] = useState(false);
  const [mapCoords, setMapCoords] = useState([6.5244, 3.3792]); // Lagos

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const email = localStorage.getItem("user_email") || "test@example.com";
        const res = await axios.get(`/bookings/?email=${email}`);
        // console.log("BOOKINGS", res.data)
        setBookings(res.data);
      } catch (e) {
        console.error("Error fetching bookings", e);
      }
    };
    fetchBookings();
  }, []);

  const upcomingBookings = bookings.filter(b => new Date(b.departure_date) >= new Date());
  const pastBookings = bookings.filter(b => new Date(b.departure_date) < new Date());

  const handleTrack = (booking) => {
    // In the future use real data
    setMapCoords([6.5244, 3.3792]);
    setMapOpen(true);
  };

  const handleOpenFeedbackModal = (booking) => {
    setSelectedBooking(booking);
    setFeedbackModalOpen(true);
  };

  const renderWideCard = (b) => (
    <Stack spacing={2} mt={1}>
      <Card key={b.booking_id || b.id}>
        <CardContent>
          <Typography variant="h6">{b.from_location} → {b.to_location}</Typography>
          <Typography color="text.secondary">{b.from_street} → {b.to_street}</Typography>

          <Typography>Date: {b.departure_date} — Time: {b.departure_time}</Typography>
          <Typography>Status: {b.status}</Typography>
          <Typography>Passengers: {b.num_of_pass}</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Booking ID: {b.booking_id}
          </Typography>

          <Stack direction="row" spacing={1} mt={1}>
            {b.feedback_submitted === true && (
              <Button size="small" variant="outlined" onClick={() => handleOpenFeedbackModal(b)}>Feedback</Button>
            )}
            <Button size="small" variant="contained" onClick={() => handleTrack(b)}>Track</Button>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );

  const renderCard = (b) => ( 
      <Grid item xs={12} md={12} key={b.id}>
        <BookingCard key={b.booking_id || b.id} booking={b}/>
        </Grid>
        )
        {/* <Card key={b.booking_id || b.id} sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
          <Box>
            <Typography variant="h6">{b.from_location} → {b.to_location}</Typography>
            <Typography>{b.departure_date} at {b.departure_time}</Typography>
            <Typography>Seats: {b.passenger_count} | Status: {b.status}</Typography>
          </Box>
          <Stack direction="row" spacing={1} alignSelf="center">
            <Button size="small" variant="contained" onClick={() => handleTrack(b)}>Track</Button>
            <Button size="small" variant="outlined" onClick={() => handleOpenFeedbackModal(b)}>Feedback</Button>
          </Stack>
        </Card>
      ); */}

  const BookingList = ({ title, data }) => {
    
    const con = viewStyle === 'compact' 
    return (
    <>
      <Typography variant="h6">{title}</Typography>
      <Divider sx={{ my: 2 }} />
      
      <Grid container={con} spacing={4}>
      {data.map(b => viewStyle === 'compact' ? 
          renderCard(b) 
          : renderWideCard(b))}
      </Grid>
      {/* </Stack> */}
    </>
  );}

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4">My Bookings</Typography>
        <ToggleButtonGroup
          value={viewStyle}
          exclusive
          onChange={(e, val) => val && setViewStyle(val)}
          size="small"
        >
          <ToggleButton value="compact">Compact</ToggleButton>
          <ToggleButton value="wide">Wide</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <Divider sx={{ my: 2 }} />

      <BookingList title="Upcoming Trips" data={upcomingBookings} />
      <BookingList title="Past Trips" data={pastBookings} />

      <Modal open={mapOpen} onClose={() => setMapOpen(false)}>
        <Box sx={{ width: '90%', mx: 'auto', mt: 15, bgcolor: 'white' }}>
          <MapView coordinates={mapCoords} />
        </Box>
      </Modal>

      {selectedBooking && (
        <FeedbackDialog
          open={feedbackModalOpen}
          onClose={() => setFeedbackModalOpen(false)}
          booking={selectedBooking}
          onSubmit={(feedback) => {
            console.log("Feedback submitted:", feedback);
          }}
        />
      )}
    </Box>
  );
}



    // <Stack spacing={2} mt={1}>
    //   <Card key={b.booking_id || b.id}>
    //     <CardContent>
    //       <Typography variant="h6">{b.from_location} → {b.to_location}</Typography>
    //       <Typography>Date: {b.departure_date} — Time: {b.departure_time}</Typography>
    //       <Typography>Status: {b.status}</Typography>
    //       <Typography>Passengers: {b.passenger_count}</Typography>
    //       <Stack direction="row" spacing={1} mt={1}>
    //         {/* <Button onClick={() => openFeedbackModal(booking)}>Leave Feedback</Button> */}
    //         {b.feedback_submitted === true  && (
    //           <Button size="small" variant="outlined" onClick={() => handleOpenFeedbackModal(b)}>Feedback</Button>
    //         )}
    //         <Button size="small" variant="contained" onClick={() => handleTrack(b)}>Track</Button>
    //       </Stack>
    //     </CardContent>
    //   </Card>
    // </Stack>




  // const upcomingBookings = [
  //   {
  //     id: 'C789',
  //     from_location: 'Enugu',
  //     to_location: 'Jos',
  //     departure_date: '2025-05-01',
  //     departure_time: '07:30 AM',
  //     status: 'completed',
  //     isUpcoming: false,
  //     feedbackGiven: true,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-05-01T12:00:00Z'
  //   },
  //   {
  //     id: 'G381',
  //     from_location: 'Imo',
  //     to_location: 'Abuja',
  //     departure_date: '2025-06-30',
  //     departure_time: '07:30 AM',
  //     status: 'completed',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-06-31T12:00:00Z'
  //   },
  //   {
  //     id: 'Q442',
  //     from_location: 'Kaduna',
  //     to_location: 'Ibadan',
  //     departure_date: '2025-05-01',
  //     departure_time: '07:30 AM',
  //     status: 'completed',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-05-01T12:00:00Z'
  //   },
  //   {
  //     id: 'D012',
  //     from_location: 'Benin',
  //     to_location: 'Ibadan',
  //     departure_date: '2025-04-18',
  //     departure_time: '05:00 PM',
  //     status: 'cancelled',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-04-18T12:00:00Z'
  //   },

  //   {
  //     id: 'F132',
  //     from_location: 'Niger',
  //     to_location: 'Cross River',
  //     departure_date: '2025-05-12',
  //     departure_time: '05:00 PM',
  //     status: 'completed',
  //     isUpcoming: false,
  //     feedbackGiven: true,
  //     feedbackResolved: true,
  //     feedbackDeadline: '2025-05-13T12:00:00Z'
  //   },
  // ];


