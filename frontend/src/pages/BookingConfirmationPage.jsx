
import { useState, useEffect } from "react";

import { Box, Typography, Paper, Button, 
  TextField, Alert, Divider, // Card, CardContent 
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import CheckCircle from "@mui/icons-material/CheckCircle";
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

import axios from "../api/axios"; 


const BookingStatus = ({error, result, handleCheckStatus, lookupId, setLookupId})=> {


  return (
        <>
          <TextField
          label="Enter Booking ID"
          fullWidth
          sx={{ my: 2 }}
          value={lookupId}
          onChange={(e) => setLookupId(e.target.value)}
        />
        <Button variant="contained" fullWidth 
        disabled={!lookupId} onClick={handleCheckStatus}>
          Check Confirmation Status
        </Button>

        {result && (
          <Alert sx={{ mt: 2 }} severity={result === "success" ? "success" : "info"}>
            Status: {result.toUpperCase()}
          </Alert>
        )}

        {error && (
          <Alert sx={{ mt: 2 }} severity="error">
            {error}
          </Alert>
        )}

        <Typography variant="body2" sx={{ my: 2 }}  color="text.primary">
          Bookings are typically confirmed immediately after payment is processed. 
          If your status shows "pending," please try again shortly or contact support.
        </Typography>
        <Divider sx={{ my: 4 }} />
        </>
  )

}



export default function BookingConfirmationPage() {
  const [lookupId, setLookupId] = useState("");
  const [result, setResult] = useState(null);
  const [paymentStatus, setPaymentStatus] = useState("pending");

  const [error, setError] = useState(null);
  const { state } = useLocation();
  let booking = state?.booking;
  const navigate = useNavigate();


   const handleCheckStatus = async () => {
    setResult(null);
    setError(null);
    try {
      const res = await axios.get(`/payments/status/${lookupId}/`);
      setResult(res.data.status);
    } catch (err) {
      console.error("Lookup failed:", err);
      setError("Booking not found or payment not initiated.");
    }
  };


  const bookingStatusProps = {error, result, handleCheckStatus, lookupId, setLookupId}
  let bookedItem = localStorage.getItem("booking");
  try{
    bookedItem = JSON.parse(bookedItem);
  } catch {
    localStorage.removeItem('booking')
    bookedItem = null;
  }
  // bookedItem = null;

  let summary = null;
  // useEffect(()=>{
  useEffect(()=>{
      if (!booking && bookedItem) return
      const interval = setInterval(async () => {
      try {
          const res = await axios.get(`/payments/status/${booking.booking_id}/`);
          // console.log("res.data.status", res.data.status)
          if (res.data.status === "success") {
            setPaymentStatus("completed");
            clearInterval(interval); // stop polling
            }
          } catch (err) {
              console.log("status check failed", err);
            }
        }, 1000); // every 1 (second)s
        
        return () => clearInterval(interval); // cleanup on unmount
  });



  if (booking) {
    const JsonBooking = JSON.stringify(booking);
    localStorage.setItem("booking", JsonBooking)
    // console.log("booking", booking, )
  }
  else if (bookedItem) {
    booking = bookedItem
    // localStorage.removeItem('booking')
    // console.log("bookedItem booking", !booking, !!bookedItem, booking)

  } else {
    // console.log("RETURN booking", booking)
    // if (!booking) 
    return (
     <Box sx={{ py: 0, px:4, maxWidth: 600, mx: "auto" }}>
        <BookingStatus {...bookingStatusProps} />
        <Typography>No booking found.</Typography>
     </Box>
    )
  }
  summary = booking.trip_summary;
  const tranState = booking 
  // const status = booking.status 
  // console.log("tranState", tranState)
  // }, [])
  

  return (
     <Box sx={{ py: 0, px:4, maxWidth: 600, mx: "auto" }}>
      <BookingStatus {...bookingStatusProps} />

      <Paper sx={{ p: 3 }} elevation={4}>
        <Box display="flex" alignItems="center" mb={2}>
          <CheckCircleOutlineIcon color="success" sx={{ mr: 1 }} />
          <Typography variant="h5">Booking Confirmed</Typography>
        </Box>

        <Typography variant="subtitle1" gutterBottom>
          Booking ID: <strong>{booking.booking_id}</strong>
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6">
          <strong>From:</strong> {summary.from.state} — <Typography variant="caption">{summary.from.stop}</Typography>
        </Typography>
        <Typography>
          <strong>To:</strong> {summary.to.state} — <Typography variant="caption">{summary.to.stop}</Typography>
        </Typography>
        <Typography>
          <strong>Date:</strong> {summary.departure_date}
        </Typography>
        <Typography>
          <strong>Time:</strong> {summary.departure_time}
        </Typography>
        <Typography>
          <strong>Seats:</strong> {summary.seats}
        </Typography>
        <Typography>
          <strong>Fare per Seat:</strong> ₦{summary.fare_per_seat}
        </Typography>
        <Typography sx={{ mt: 1, fontWeight: "bold" }}>
          Total Fare: ₦{summary.total_fare}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Button variant="contained" 
        disabled={paymentStatus === "completed"}
        color={paymentStatus === "completed" ? "success" : "primary"}  fullWidth 
        onClick={() => navigate("/book/payment/", { state: tranState })}
        startIcon={paymentStatus === "completed" ? <CheckCircle color="success" /> : null}
        >
          {paymentStatus === "completed" ? "Payment Complete" : "Proceed to Payment"}
        </Button>

        {/* <Button
          variant="contained"
          color="primary"
          fullWidth
          onClick={() => navigate("/book/payment/", { state: tranState })}
        >
          Proceed to Payment
        </Button> */}
      </Paper>
    </Box>
  );
  
  }
//   return (

//       <Box p={4}>
//         <Typography variant="h4" gutterBottom>Booking Confirmation</Typography>
//         <Card>
//           <CardContent>
//             <Typography>Booking ID: {booking.booking_id}</Typography>
//             <Typography>Status: {booking.status}</Typography>
//           <hr />
//           <Typography>From: {summary.from.state}</Typography> <Typography variant="subtitle2">{summary.from.stop}</Typography>
//           <Typography>To: {summary.to.state}</Typography> <Typography variant="subtitle2">{summary.to.stop}</Typography> 
//           <Typography>Date: {summary.departure_date}</Typography>
//           <Typography>Time: {summary.departure_time}</Typography>
//           <Typography>Seats: {summary.seats}</Typography>
//           {/* <Typography>Seats: {summary.passenger_count}</Typography> */}
//           <Typography>Fare per seat: ₦{summary.fare_per_seat}</Typography>
//           <Typography fontWeight="bold">Total Fare: ₦{summary.total_fare}</Typography>
//           {/* <Typography>Bus: {summary.bus_number}</Typography>
//           <Typography>Driver: {summary.driver_name}</Typography> */}
//         </CardContent>
//       </Card>
//     </Box>
//   );
// }
