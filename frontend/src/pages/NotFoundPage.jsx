import { Box, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <Box sx={{ p: 4, textAlign: 'center' }}>
      <Typography variant="h2">404</Typography>
      <Typography variant="h5" gutterBottom>Page Not Found</Typography>
      <Typography variant="body1">Oops! No trips heading in that direction, Go back to home page.</Typography>
      <Button variant="contained" color="primary" sx={{ mt: 3 }} component={Link} to="/">
        Return Home
      </Button>
    </Box>
  );
}
