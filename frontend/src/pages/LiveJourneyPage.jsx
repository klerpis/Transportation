import { Box, Typography, Paper } from '@mui/material';
// import { Snackbar, Alert } from "@mui/material";

import MapView from '../components/map/MapView'; // same Leaflet map we used


import { useParams } from "react-router-dom";

export default function LiveJourneyPage() {
  const { tripId } = useParams(); // from /live/:tripId

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Live Journey Tracking
      </Typography>
      <Typography variant="body2" gutterBottom>
        Track your vehicle in real time as it moves between locations.
      </Typography>

      <Paper elevation={7} sx={{ mt: 3, height: 400 }}>
        <MapView tripId={tripId} />
      </Paper>
    </Box>
  );
}
