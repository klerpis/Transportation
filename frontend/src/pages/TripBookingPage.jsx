
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Box,
  Typography, Card, CardContent,
  Grid, Button, CircularProgress
} from "@mui/material";
import axios from "../api/axios";
import TripSearchForm from "../components/TripSearchForm";
import BookOnlineIcon from '@mui/icons-material/BookmarkAdd';
import TripModal from '../components/TripModal';



export default function TripBookingPage() {
  // const [trips, setTrips] = useState([]);
  const [trips, setTrips] = useState([]);
  const [searching, setSearching] = useState(false);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const navigate = useNavigate();

  const [form, setForm] = useState({
      email: "",
      first_name: "",
      last_name: "",
      num_of_pass: 1,
    });


  //   const trips = [
  //   {
  //     id: 'C789',
  //     from_location: 'Enugu',
  //     to_location: 'Jos',
  //     trip_departure_date: '2025-05-01',
  //     trip_departure_time: '07:30 AM',
  //     status: 'pending',
  //     isUpcoming: false,
  //     feedbackGiven: true,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-05-01T12:00:00Z'
  //   },
  //   {
  //     id: 'G381',
  //     from_location: 'Imo',
  //     to_location: 'Abuja',
  //     trip_departure_date: '2025-06-30',
  //     trip_departure_time: '07:30 AM',
  //     status: 'pending',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-06-31T12:00:00Z'
  //   },
  //   {
  //     id: 'Q442',
  //     from_location: 'Kaduna',
  //     to_location: 'Ibadan',
  //     trip_departure_date: '2025-05-01',
  //     trip_departure_time: '07:30 AM',
  //     status: 'pending',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-05-01T12:00:00Z'
  //   },
  //   {
  //     id: 'D012',
  //     from_location: 'Benin',
  //     to_location: 'Ibadan',
  //     trip_departure_date: '2025-04-18',
  //     trip_departure_time: '05:00 PM',
  //     status: 'pending',
  //     isUpcoming: false,
  //     feedbackGiven: false,
  //     feedbackResolved: false,
  //     feedbackDeadline: '2025-04-18T12:00:00Z'
  //   },

  //   {
  //     id: 'F132',
  //     from_location: 'Niger',
  //     to_location: 'Cross River',
  //     trip_departure_date: '2025-05-12',
  //     trip_departure_time: '05:00 PM',
  //     status: 'pending',
  //     isUpcoming: false,
  //     feedbackGiven: true,
  //     feedbackResolved: true,
  //     feedbackDeadline: '2025-05-13T12:00:00Z'
  //   },
  // ];

  
  const validateForm = () => {
    const errors = {};
    if (!form.email) errors.email = "Email is required";
    if (!form.first_name) errors.first_name = "First name is required";
    if (!form.last_name) errors.last_name = "Last name is required";
    if (!form.num_of_pass || form.num_of_pass <= 0)
      errors.num_of_pass = "Passenger count must be at least 1";
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };



  const handleSearch = async ({ from_, to, date }) => {
    setSearching(true);
    try {
      const res = await axios.get(`/trips/?from=${from_}&to=${to}&date=${date}`);
      // console.log("TRIP SEARCH === ", res.data)

      setTrips(res.data);
      
    } catch (e) {
      console.log("TRIP SEARCH ERROR === ", e)
      alert("Error fetching trips");
    } finally {
      setSearching(false);
    }
  };

  const handleBookClick = (trip) => {
    setForm({
      email: "",
      first_name: "",
      last_name: "",
      num_of_pass: 1,
      
    })

    setFormErrors({
      email: "",
      first_name: "",
      last_name: "",
      num_of_pass: 0,
    })
    setSelectedTrip(trip);
    setShowModal(true);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: name === "num_of_pass" ? parseInt(value) : value }));
  };

const submitBooking = async () => {
  if (!validateForm()) return;
  try {
    const payload = {
      ...form,
      departure_date: selectedTrip.trip_departure_date,
      departure_time: selectedTrip.trip_departure_time,
      location_from: selectedTrip.from_location,
      destination_to: selectedTrip.to_location,
      trip_id: selectedTrip.trip_id,
      // fare: selectedTrip.fare_per_seat
      // status: selectedTrip.status,
      // fare_per_seat: selectedTrip.fare_per_seat,

    };
    // console.log('PAYLOAD ', payload)
    const res = await axios.post("/bookings/create/", payload);
    alert(`✅ Booking Confirmed! Booking ID: ${res.data.booking_id}`);
    // console.log('Booking Confirmed ✅ . Please try again', res.data)
    setShowModal(false);
    navigate("/book/confirmed", { state: { booking: res.data } });
  } catch(e) {
    // navigate("/book/confirmed");
    console.log('❌ Booking failed. Please try again', e)
    alert("❌ Booking failed. Please try again.");
  }
};

  // console.log("selectedTrip", selectedTrip, !!trips.length, trips.length)
  // console.log("JUSTTrip", trips, trips.length)
  const tripProps = {showModal, setShowModal, handleFormChange, 
                    form, submitBooking, selectedTrip, formErrors}
  
  return (
    <Box p={4}>
      <Typography variant="h4" mb={3}>Search & Book a Trip</Typography>

      <TripSearchForm onSearch={handleSearch} />

      {searching ? (
        <Box mt={4}><CircularProgress /></Box>
      ) : (!!trips.length ? (
        <Grid container spacing={2} mt={2}>
          {trips.map((trip) => (
            <Grid item xs={12} sm={6} md={4} key={trip.trip_id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{trip.from_location} → {trip.to_location}</Typography>
                  <Typography variant="subtitle2">Date: {trip.trip_departure_date}</Typography>
                  <Typography variant="subtitle2">Time: {trip.trip_departure_time}</Typography>
                  <Typography variant="overline" mr={2}>Status: {trip.status}</Typography>
                  <Button
                    variant="outlined"
                    color="primary"
                    sx={{ mt: 2 }}
                    startIcon={<BookOnlineIcon />}
                    onClick={() => handleBookClick(trip)}
                  >
                    Book This Trip
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid> 
        ) : (
          <Box mt={4}>
            <Typography variant="h6">No Trips for this location/date </Typography>
          </Box>
        )
      )}
    
      {/* Booking Modal */}
      <TripModal {...tripProps} />

    </Box>
  );
}




// import { Box, Typography, Grid, 
//         TextField, MenuItem, Button, Paper,
//         } from '@mui/material';
        
// import { useState } from 'react';

// import { useNavigate } from 'react-router-dom';



// const routes = [
//   { from: 'Lagos', to: 'Abuja', fare: 7500 },
//   { from: 'Ibadan', to: 'Enugu', fare: 5200 },
// ];

// const times = {
//   'Lagos-Abuja': ['08:00', '12:00', '16:00'],
//   'Ibadan-Enugu': ['09:00', '13:30'],
// };

// export default function TripBookingPage() {
//   const [route, setRoute] = useState('');
//   const [date, setDate] = useState('');
//   const [time, setTime] = useState('');
//   const [passengers, setPassengers] = useState(1);
//   const navigate = useNavigate();
  
//   const selectedRoute = routes.find(
//     (r) => `${r.from}-${r.to}` === route
//   );
  
//   const handleSubmit = () => {
    // console.log('Booking Details:', {
//       route,
//       date,
//       time,
//       passengers,
//       fare: selectedRoute?.fare,
//     });

//     // navigate('/book/payments')
//     // Redirect or show confirmation modal
//   };

//   return (
//     <Box sx={{ p: 3 }}>
//       <Typography variant="h4" gutterBottom>
//         Book a Trip
//       </Typography>

//       <Paper sx={{ p: 3 }}>
//         <Grid container spacing={2}>
//           <Grid item xs={6}>
//             <TextField
//               fullWidth
//               select
//               label="Select Route"
//               value={route}
//               onChange={(e) => setRoute(e.target.value)}
//             >
//               {routes.map((r, i) => (
//                 <MenuItem key={i} value={`${r.from}-${r.to}`}>
//                   {r.from} → {r.to}
//                 </MenuItem>
//               ))}
//             </TextField>
//           </Grid>

//           <Grid item xs={6}>
//             <TextField
//               fullWidth
//               label="Travel Date"
//               type="date"
//               InputLabelProps={{ shrink: true }}
//               value={date}
//               onChange={(e) => setDate(e.target.value)}
//             />
//           </Grid>

//           {route && (
//             <Grid item xs={6}>
//               <TextField
//                 fullWidth
//                 select
//                 label="Departure Time"
//                 value={time}
//                 onChange={(e) => setTime(e.target.value)}
//               >
//                 {(times[route] || []).map((t, i) => (
//                   <MenuItem key={i} value={t}>{t}</MenuItem>
//                 ))}
//               </TextField>
//             </Grid>
//           )}

//           <Grid item xs={6}>
//             <TextField
//               fullWidth
//               label="Passengers"
//               type="number"
//               value={passengers}
//               onChange={(e) => setPassengers(Number(e.target.value))}
//             />
//           </Grid>

//           {selectedRoute && (
//             <Grid item xs={12}>
//               <Typography variant="h6">
//                 Total Fare: ₦{selectedRoute.fare * passengers}
//               </Typography>
//             </Grid>
//           )}

//           <Grid item xs={12}>
//             <Button variant="contained" fullWidth onClick={handleSubmit}>
//               Proceed to Payment
//             </Button>
//           </Grid>
//         </Grid>
//       </Paper>
//     </Box>
//   );
// }
