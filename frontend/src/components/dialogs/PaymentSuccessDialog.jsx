import { 
        Dialog, DialogTitle,
        DialogContent,DialogActions,Button,Typography,CheckCircleOutline,
        } from '@mui/material';
import { green } from '@mui/material/colors';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

export default function PaymentSuccessDialog({ open, onClose }) {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>
        <CheckCircleIcon sx={{ color: green[500], fontSize: 40, mr: 1 }} />
        Payment Successful
      </DialogTitle>
      <DialogContent>
        <Typography>Your trip has been booked successfully!</Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} autoFocus>OK</Button>
      </DialogActions>
    </Dialog>
  );
}
