import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Box, Typography, Paper, Button, Divider, MenuItem, Select, InputLabel, FormControl
} from "@mui/material";
import axios from "../api/axios";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import CheckCircle from "@mui/icons-material/CheckCircle";




const Alert = React.forwardRef((props, ref) => (
  <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />
));




const bookingConfirmed = (booking)=> { // set for the booking confirmation page
    let bookedItem = localStorage.getItem("booking");
    try{
      bookedItem = JSON.parse(bookedItem);
    } catch {
      localStorage.removeItem('booking')
      bookedItem = null;
    }
  
    // let summary = null;
    // useEffect(()=>{
    if (booking) {
      booking.status = 'completed'
      const JsonBooking = JSON.stringify(booking);
      localStorage.setItem("booking", JsonBooking)
      // console.log("Confirmation by payment for booking", booking, booking.status)
    }
    else if (bookedItem) {
      booking = bookedItem
      booking.status = 'completed'
      const JsonBooking = JSON.stringify(booking);
      localStorage.setItem("booking", JsonBooking)
      // console.log("Confirmation by payment for booking/bookedItem ", booking, booking.status)

    }

    //  else {
      console.log("RETURN booking", booking)
    //   // if (!booking) 
    //   // return <Typography>No booking found.</Typography>;
    // }
}




export default function PaymentPage() {
  const { state } = useLocation(); // booking data
  const navigate = useNavigate();
  const [showSuccess, setShowSuccess] = useState(false);
  // console.log("PaymentPage state", state)

  const [method, setMethod] = useState("card");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("pending"); // || "pending");  // fallback to passed state
  let bookingExist = true

  if (!state || !state.booking_id) bookingExist = false
  useEffect(() => {
    // console.log("bookingExist", bookingExist, !bookingExist)
    const interval = !bookingExist ? '' : setInterval(async () => {
      try {
            const res = await axios.get(`/payments/status/${booking_id}/`);
            // console.log("res.data.status", res.data.status)
            if (res.data.status === "success") {

              setStatus("success");
              clearInterval(interval); // stop polling
              // console.log("res.data.status condition", res.data.status, interval)
              // const bookingState = {...state, status: 'completed'}
              bookingConfirmed(state) // state is the booking, in this page
              }
          } catch (err) {
              console.log("Polling failed", err);
            }
      }, 3000); // every 3 seconds

      return () => clearInterval(interval); // cleanup on unmount
    });
    
    if (!bookingExist) return <Typography>No booking data found.</Typography>;
    const { booking_id, trip_summary} = state;
    // console.log("payment page")
    
  const handlePay = async () => {
  setLoading(true);
  try {
    const res = await axios.patch(
      `/payments/update/${booking_id}/`,
      { method }
    );

    // Optional: handle backend-provided redirect
    setShowSuccess(true);
    setTimeout(() => {
        if (res.data.redirect) {
          navigate(res.data.redirect);
      } else {
        // Frontend-controlled routing based on method
        if (method === "card") navigate("/pay/card", { state });
        else if (method === "transfer") navigate("/pay/transfer", { state });
        else if (method === "cash") navigate("/pay/cash", { state });
        // else navigate("/payments/history");
      }
    }, 1800); // Slight delay before redirect

  } catch (err) {
    console.error("Payment method update failed:", err);
    alert("Failed to update payment method.");
  } finally {
    setLoading(false);
    }
  };


return (
    <Box sx={{ p: 4, maxWidth: 600, mx: "auto" }}>

      <Snackbar
        open={showSuccess}
        autoHideDuration={2000}
        onClose={() => setShowSuccess(false)}
      >
        <Alert severity="success" onClose={() => setShowSuccess(false)}>
          Payment Created!
        </Alert>
      </Snackbar>

      <Paper sx={{ p: 3 }} elevation={4}>
        <Typography variant="h5" gutterBottom>
          Complete Your Payment
        </Typography>

        <Typography gutterBottom>
          Booking ID: <strong>{booking_id}</strong>
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography>
          <strong>From:</strong> {trip_summary.from.state} — {trip_summary.from.stop}
        </Typography>
        <Typography>
          <strong>To:</strong> {trip_summary.to.state} — {trip_summary.to.stop}
        </Typography>
        <Typography>
          <strong>Seats:</strong> {trip_summary.seats}
        </Typography>
        <Typography>
          <strong>Fare per seat:</strong> ₦{trip_summary.fare_per_seat}
        </Typography>
        <Typography sx={{ mt: 1, fontWeight: "bold" }}>
          Total: ₦{trip_summary.total_fare}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <FormControl fullWidth sx={{ mb: 2 }} disabled={loading || status === "success"}>
          <InputLabel>Payment Method</InputLabel>
          <Select
            value={method}
            label="Payment Method"
            onChange={(e) => setMethod(e.target.value)}
          >
            <MenuItem disabled={loading || status === "success"} value="card">Card</MenuItem>
            <MenuItem disabled={loading || status === "success"} value="transfer">Bank Transfer</MenuItem>
            <MenuItem disabled={loading || status === "success"} value="cash">Pay with Cash</MenuItem>
          </Select>
        </FormControl>
      </Paper>

      {/* // Show status if already confirmed */}
      {status === "success" ? (
        <Alert severity="success" sx={{ mt: 2 }}>
          Payment Confirmed ✔️
        </Alert>
      ) : (
        <Button variant="contained" 
        disabled={loading || status === "success"} 
        color="success" fullWidth onClick={handlePay}
        startIcon={status === "success" ? <CheckCircle color="success" /> : null}
        >
          {loading ? "Processing..." : status === "success" ? "Payment Complete" : "Confirm Payment"}
        </Button>
      )}

      
    </Box>
  );
}












// import {
//   Box, Typography, Paper, TextField, Grid,
//   Button, RadioGroup, Radio, FormControlLabel, Divider,
// } from '@mui/material';

// import { useState } from 'react';
// import PaymentSuccessDialog from '../components/dialogs/PaymentSuccessDialog';


// export default function PaymentPage() {
//     const [successOpen, setSuccessOpen] = useState(false);

//     const handlePayNow = () => {
//         // simulate payment success
//         setSuccessOpen(true);
//     };
//   return (
//     <Box sx={{ p: 3 }}>
//       <Typography variant="h4" gutterBottom>
//         Payment Checkout
//       </Typography>

//       <Grid container spacing={4}>
//         {/* Trip Summary */}
//         <Grid item xs={12} md={6}>
//           <Paper sx={{ p: 3 }}>
//             <Typography variant="h6">Trip Summary</Typography>
//             <Divider sx={{ my: 1 }} />
//             <Typography variant="body1">From: Lagos</Typography>
//             <Typography variant="body1">To: Abuja</Typography>
//             <Typography variant="body1">Date: 2025-06-22</Typography>
//             <Typography variant="body1">Passenger: Marvelous Nust</Typography>
//             <Typography variant="h6" sx={{ mt: 2 }}>
//               Total: ₦7,500
//             </Typography>
//           </Paper>
//         </Grid>

//         {/* Payment Form */}
//         <Grid item xs={12} md={6}>
//           <Paper sx={{ p: 3 }}>
//             <Typography variant="h6">Enter Payment Details</Typography>
//             <Divider sx={{ my: 1 }} />

//             <TextField fullWidth label="Cardholder Name" sx={{ mb: 2 }} />
//             <TextField fullWidth label="Card Number" sx={{ mb: 2 }} />
//             <Grid container spacing={2}>
//               <Grid item xs={6}>
//                 <TextField fullWidth label="Expiry Date" />
//               </Grid>
//               <Grid item xs={6}>
//                 <TextField fullWidth label="CVV" />
//               </Grid>
//             </Grid>

//             <Typography variant="subtitle1" sx={{ mt: 3 }}>
//               Or choose another payment method:
//             </Typography>

//             <RadioGroup defaultValue="card">
//               <FormControlLabel value="card" control={<Radio />} label="Credit/Debit Card" />
//               <FormControlLabel value="transfer" control={<Radio />} label="Bank Transfer" />
//               <FormControlLabel value="wallet" control={<Radio />} label="Wallet Balance" />
//             </RadioGroup>

//             <Button variant="contained" color="primary" sx={{ mt: 3 }} fullWidth onClick={handlePayNow}>
//               Pay Now
//             </Button>
//           </Paper>
//         </Grid>
//       </Grid>
//     <PaymentSuccessDialog open={successOpen} onClose={() => setSuccessOpen(false)} />
//     </Box>
//   );
// }
