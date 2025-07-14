import React from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { Box, Typography, Divider } from '@mui/material';

export default function DynamicPaymentPage() {
  const { method } = useParams(); // card, transfer, cash
  const { state } = useLocation(); // contains booking/trip info

  const renderForm = () => {
    switch (method) {
      case 'card':
        return <Typography>🔐 Card Payment Form</Typography>;
      case 'transfer':
        return <Typography>🏦 Bank Account Details for Transfer</Typography>;
      case 'cash':
        return <Typography>🧾 Pay at terminal – show this booking ID: {state?.booking_id}</Typography>;
      default:
        return <Typography>Unknown payment method</Typography>;
    }
  };

  return (
    <Box p={4} maxWidth={600} mx="auto">
      <Typography variant="h5">Payment Method: {method.toUpperCase()}</Typography>
      <Divider sx={{ my: 2 }} />
      {renderForm()}
    </Box>
  );
}
