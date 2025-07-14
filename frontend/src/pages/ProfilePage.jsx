import { Box, Typography, 
  // Divider, 
  Rating, Snackbar, Alert, Slide, Paper, TextField, Button, Avatar, Grid } from '@mui/material';
import { useState, useEffect } from 'react';

import axios from '../api/axios';

import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';



const pastFeedback = [
  {
    journeyId: 1,
    from: 'Lagos',
    to: 'Abuja',
    date: '2025-06-10',
    rating: 4,
    text: 'Driver was professional. Smooth ride.',
  },
  {
    journeyId: 2,
    from: 'Ibadan',
    to: 'Enugu',
    date: '2025-06-05',
    rating: 5,
    text: 'Excellent timing and comfort.',
  },
];

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    username: '',
    firstname:'',
    lastname:'',
    email: '',
    phonenumber: '08012345678',
    bio: '',
  });
  // avatar:''
  const [feedbacks, setFeedbacks] = useState([]);

  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);

  
  const handleSave = async () => {
    try {
      const cleanProfileData = (data) => {
        const cleaned = {};
        Object.entries(data).forEach(([key, value]) => {
          if (value !== "" && value !== null && value !== undefined) {
            cleaned[key] = value;
          }
        });
        return cleaned;
      };
      const cleanedProfile = cleanProfileData(profile)

    await axios.put("/user/profile/", cleanedProfile);
    // alert("✅ Profile updated");
    setShowSuccess(true);

  } catch (error) {
    console.log(error)
    // alert("❌ Failed to save changes");
    setShowError(true);
  }
};

useEffect(() => {
  const fetchProfile = async () => {
    try {
      const res = await axios.get("/user/profile/");
      // console.log("PROFILE DATA", res.data)
      setProfile(res.data);
    } catch (error){
      console.log(error)
      alert("Failed to fetch profile");
    }
  };

  fetchProfile();
  
  const email = localStorage.getItem("user_email");
  try {
    axios.get(`/feedbacks/?email=${email}`).then(res => {
      console.log("res.data for feedback", res.data)
      setFeedbacks(res.data)
    });
  } catch (error) {
    console.log(error)    
  }

}, []);



  return (
    <Box sx={{ py: 0, px:4, maxWidth: 600, mx: "left" }}>
    
      <Typography variant="h4" gutterBottom>
        My Profile
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Update your personal information and preferences.
      </Typography>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, my: 3 }}>
        <Avatar sx={{ width: 64, height: 64 }}>J</Avatar>
        <Typography>Change Picture (optional)</Typography>
      </Box>
      <Grid container xs={12} md={6}>
        <Grid container xs={12} md={6}>
          <TextField
            label="Username" fullWidth sx={{ mb: 2 }}
            value={profile.username} onChange={(e) => setProfile({ ...profile, username: e.target.value })}
            />
          <TextField label="Email" fullWidth sx={{ mb: 2 }} value={profile.email} 
            onChange={(e) => setProfile({ ...profile, email: e.target.value })}
            />
          <TextField label="First Name" fullWidth sx={{ mb: 2 }} value={profile.firstname} 
            onChange={(e) => setProfile({ ...profile, firstname: e.target.value })}
            />
          <TextField label="Last Name" fullWidth sx={{ mb: 2 }} value={profile.lastname} 
            onChange={(e) => setProfile({ ...profile, lastname: e.target.value })}
            />
          <TextField label="Phone" fullWidth sx={{ mb: 2 }} value={profile.phonenumber} 
            onChange={(e) => setProfile({ ...profile, phonenumber: e.target.value })}
          />
          <TextField label="Bio" multiline rows={4} fullWidth sx={{ mb: 2 }} value={profile.bio} 
            onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
          />

          <Button variant="contained" onClick={handleSave}>
            Save Changes
          </Button>
        </Grid>
      </Grid>

      <Typography variant="h5" sx={{ mt: 4 }}>
        My Past Feedback
      </Typography>
      {/* {pastFeedback.map((f, i) => ( */}
      {feedbacks.map((f, i) => (

        <Paper key={i} sx={{ p: 2, mt: 2 }}>
          <Typography variant="subtitle1">
            {f.from_location} → {f.to_destination}   
            <Typography variant="caption" sx={{ ml: 2 }}>
              on {f.departure_date} at {f.departure_time}
            </Typography>
          </Typography>
          <Rating value={f.rating} readOnly />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {f.comment}
          </Typography>
        </Paper>
      ))}

    <Snackbar
      open={showSuccess}
      autoHideDuration={3000}
      onClose={() => setShowSuccess(false)}
      anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      TransitionComponent={Slide}
    >
      <Alert
        icon={<CheckCircleIcon fontSize="inherit" />}
        severity="success"
        variant="filled"
        sx={{
          backgroundColor: '#4caf50', // success green
          color: 'white',
          fontSize: '1rem',
          borderRadius: '8px',
          boxShadow: 3,
        }}
      >
        <Typography fontWeight={600}>
          ✅ Profile updated successfully!
        </Typography>
      </Alert>
    </Snackbar>

    <Snackbar
      open={showError}
      autoHideDuration={3000}
      onClose={() => setShowError(false)}
      anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      TransitionComponent={Slide}
    >
      <Alert
        icon={<ErrorIcon fontSize="inherit" />}
        severity="error"
        variant="filled"
        sx={{
          backgroundColor: '#d32f2f', // error red
          color: 'white',
          fontSize: '1rem',
          borderRadius: '8px',
          boxShadow: 3,
        }}
      >
        <Typography fontWeight={600}>
          ❌ Failed to update profile.
        </Typography>
      </Alert>
    </Snackbar>


    </Box>
  );
}


// {feedbacks.map((f, i) => (
//   <Paper key={i} sx={{ p: 2, mt: 2 }}>
//     <Typography variant="subtitle1">{f.from_location} → {f.destination_to}</Typography>
//     <Typography variant="caption">{f.submitted_at}</Typography>
//     <Rating value={f.rating} readOnly />
//     <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>{f.feedback_text}</Typography>
//   </Paper>
// ))}
