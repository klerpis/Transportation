import {
  Box, Button,
  Typography, TextField, 
  Stack, Modal, Divider,
} from "@mui/material";

// import { useThemeMode } from '../../contexts/ThemeContext';
import { useTheme } from '@mui/material/styles';


const TripModal = ({showModal, setShowModal, handleFormChange, 
                        form, submitBooking, selectedTrip, formErrors})=> {
      // const { mode, toggleColorMode } = useThemeMode();
      const theme = useTheme();
    return (<Modal open={showModal} onClose={() => setShowModal(false)}>
        <Box sx={{
          
          bgcolor: theme.palette.mode === 'dark' ? 'grey.900' : 'white', 
          p: 4, width: 400,
          m: 'auto', mt: 10, borderRadius: 2
        }}>
          <Typography variant="h6" gutterBottom>Passenger Info</Typography>
          <Stack spacing={2}>
            <TextField
              label="Email" error={!!formErrors.email}
              name="email" value={form.email}
              onChange={handleFormChange} fullWidth
            />
            <TextField
              label="First Name" name="first_name" error={!!formErrors.first_name}
              value={form.first_name} onChange={handleFormChange} fullWidth
            />
            <TextField
              label="Last Name" name="last_name" value={form.last_name}
              onChange={handleFormChange} fullWidth error={!!formErrors.last_name}
            />
            <TextField
              label="Passengers" name="num_of_pass" type="number" error={!!formErrors.num_of_pass}
              value={form.num_of_pass} onChange={handleFormChange} fullWidth
            />
            <Button variant="contained" onClick={submitBooking}>Confirm Booking</Button>
          </Stack>
          {/* Trip Summary Section */}
            { selectedTrip && (
                <Box my={2}>
                    <Typography variant="subtitle1">Trip Summary</Typography>
                    <Divider />
                    <Typography mt={2} fontSize={14}>
                        {selectedTrip.from_location} → {selectedTrip.to_location}
                    </Typography>
                    <Typography fontSize={14}>
                        Date: {selectedTrip.trip_departure_date} @ {selectedTrip.trip_departure_time}
                    </Typography>
                    <Typography fontSize={14}>
                        Fare per seat: ₦{selectedTrip.fare_per_seat || 5000}
                    </Typography>
                    <Typography fontSize={14} fontWeight="bold">
                        Total: ₦{(selectedTrip.fare_per_seat || 5000) * form.num_of_pass}
                    </Typography>
                </Box>
            )}
        </Box>

      </Modal>
    );
};



export default TripModal