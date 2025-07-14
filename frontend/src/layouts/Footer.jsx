
import { Box, Typography } from "@mui/material";


export default function Footer(){
    return (
        <Box sx={{ p: 2, mt: 4, textAlign: 'center' // , bgcolor: 'grey.300' 
        }}>
            <Typography variant='body2' color='textSecondary'>
                © {new Date().getFullYear()} AKTC all rights reserved.
            </Typography>
        </Box>
    );
};