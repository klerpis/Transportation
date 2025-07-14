import React, { useEffect, useState } from "react";
import { Box, Typography, Paper, Divider, Chip, Button,
  CircularProgress, TextField } from "@mui/material";
import axios from "../api/axios";
import jsPDF from "jspdf";




const generatePDF = (payment) => {
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("AKTC Payment Receipt", 20, 20);

  doc.setFontSize(12);
  doc.text(`Booking ID: ${payment.booking_id}`, 20, 40);
  doc.text(`Amount: ₦${payment.amount}`, 20, 50);
  doc.text(`Method: ${payment.method}`, 20, 60);
  doc.text(`Status: ${payment.status}`, 20, 70);
  doc.text(`Date: ${new Date(payment.created).toLocaleString()}`, 20, 80);

  doc.save(`receipt-${payment.booking_id}.pdf`);
};



export default function PaymentHistoryPage() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

// const payments = [
//   {
//     booking_id: 'TRIP-001',
//     from: 'Lagos',
//     to: 'Abuja',
//     method: 'card',
//     amount: '7500',
//     created: '2025-06-01',
//     status: 'confirmed',
//   },
//   {
//     booking_id: 'TRIP-002',
//     from: 'Ibadan',
//     to: 'Enugu',
//     method: 'card',
//     amount: '5200',
//     created: '2025-05-28',
//     status: 'Pending',
//   },
// ];



  useEffect(() => {
    axios.get("/payments/history/")
      .then((res) => setPayments(res.data))
      .catch(() => alert("Could not load payment history."))
      .finally(() => setLoading(false));
  }, []);

  const filtered = payments.filter(p =>
    p.booking_id.toLowerCase().includes(search.toLowerCase())
  );


  return (
    <Box sx={{ p: 4, maxWidth: 700, mx: "auto" }}>
      <Typography variant="h4" gutterBottom>
        Payment History
      </Typography>

      <TextField
          label="Search by Booking ID"
          variant="outlined"
          fullWidth
          sx={{ mb: 3 }}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />


      {loading ? <CircularProgress /> : (
        payments.length === 0 ? (
          <Typography>No payment records found.</Typography>
        ) : (
          filtered.map((pay, i) => (
            <Paper key={i} sx={{ p: 2, my: 2 }}>
              <Typography>
                Booking ID: <strong>{pay.booking_id}</strong>
              </Typography>
              <Typography>
                Method: {pay.method.toUpperCase()} • ₦{pay.amount}
              </Typography>
              <Typography>
                Date: {new Date(pay.created).toLocaleString()}
              </Typography>

              <Divider sx={{ my: 1 }} />
              <Chip
                label={pay.status.toUpperCase()}
                color={pay.status === "success" ? "success" : "warning"}
              />
              <Button
                size="small"
                variant="outlined"
                sx={{ ml: 2}}
                onClick={() => generatePDF(pay)}
              >
                Download Receipt
              </Button>

            </Paper>
          ))
        )
      )}
    </Box>
  );
}



// import { Box, Typography, Paper, Divider } from '@mui/material';

// const mockHistory = [
//   {
//     id: 'TRIP-001',
//     from: 'Lagos',
//     to: 'Abuja',
//     amount: '₦7500',
//     date: '2025-06-01',
//     status: 'Success',
//   },
//   {
//     id: 'TRIP-002',
//     from: 'Ibadan',
//     to: 'Enugu',
//     amount: '₦5200',
//     date: '2025-05-28',
//     status: 'Success',
//   },
// ];

// export default function PaymentHistoryPage() {
//   return (
//     <Box sx={{ p: 3 }}>
//       <Typography variant="h4" gutterBottom>Payment History</Typography>
//        <Divider sx={{ my: 1 }} />
//       {mockHistory.map((entry) => (
//         <Paper key={entry.id} sx={{ p: 2, mb: 2 }}>
//           <Typography variant="subtitle1">{entry.from} → {entry.to}</Typography>
//           <Typography>Amount: {entry.amount}</Typography>
//           <Typography>Date: {entry.date}</Typography>
//           <Typography>Status: {entry.status}</Typography>
//         </Paper>
//       ))}
//     </Box>
//   );
// }
