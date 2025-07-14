import { Grid, Typography, Card, Box, Paper, Container, 
         CardContent, CardMedia, Button, Rating, Avatar, TextField,
        Accordion, AccordionSummary, AccordionDetails
        } from '@mui/material';

        import ExpandMoreIcon from '@mui/icons-material/ExpandMore';


import ShieldIcon from '@mui/icons-material/Security';
import GpsFixedIcon from '@mui/icons-material/GpsFixed';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import HeadsetMicIcon from '@mui/icons-material/HeadsetMic';


import { useNavigate } from 'react-router-dom';


import { HomePageBookingStrip } from '../components/BookingStrip';
import ContactSupport from '../components/ContactSupport';

import { useState, useEffect } from 'react';
import axios from '../api/axios';
// import { useThemeMode } from '../contexts/ThemeContext';
import { useTheme } from '@mui/material/styles';

import crossRiverImage from '../logo512.png';


export default function HomePage(){
    const navigate = useNavigate();
    const [reviews, setReviews] = useState([])
    // const { mode, toggleColorMode } = useThemeMode();
    const theme = useTheme();


    useEffect(() => {

        async function getReviews() {
            try {
                const res = await axios.get("/reviews/");
                setReviews(res.data)
                // alert("✅ Feedback submitted!");
                // onClose();
                // refreshBookings(); // optional refetch to update UI
            } catch (e) {
                console.log('reviews delayed')
                // alert(e.response?.data?.error || "❌ Could not submit feedback");
            }
        } 
    getReviews()
    }, [])


    return (
        <Container maxWidth='lg'>
            {/* HERO SECTION */}
            <Box 
                // bgcolor='secondary'
                sx={{
                    py: { xs: 6, md: 10 },
                    textAlign: 'center',
                    backgroundColor: theme.palette.mode === 'dark' ? 'grey.800' : '#f0f4ff',
                    // backgroundColor: 'bgcolor.primary',
                    // color: 'grey.1000',
                    borderRadius: 2,
                    mt: 4,
                }}>
                <Typography variant="h2" sx={{ fontWeight: 'bold', mb: 2 }}>
                Welcome to AkwaIbom Transport Corporation
                </Typography>
                <Typography variant="h6" sx={{ color: 'text.secondary', mb: 4 }}>
                Book your next journey with ease and confidence.
                </Typography>
                <Button variant="contained" size="large" color="primary"
                    onClick={()=> navigate('/book')}>
                Start Booking
                </Button>
            </Box>

            {/* BOOKING STRIP */}
                <Paper
                    elevation={4}
                    sx={{
                        mt: 6,
                        p: { xs: 2, md: 4 },
                        borderRadius: 2,
                        // backgroundColor: '#ffffff',
                    }}>
                    <Typography variant="h5" gutterBottom>
                        Book a Trip
                    </Typography>
                    <HomePageBookingStrip />
                </Paper>

            {/* FEATURED DESTINATIONS */}
            <Box sx={{ mt: 8 }}>
            <Typography variant="h4" gutterBottom>
                Featured Destinations
            </Typography>

            <Grid container spacing={4}>
                {[
                {
                    name: 'Cross River',
                    image: 'https://imgs.search.brave.com/m6lJAI8KxgKxDU4j_z-6ZRF-6pl5D0e-nzpE1pzySQk/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9oNy5h/bGFteS5jb20vY29t/cC8yQ0JHR0s5L3No/YXBlLW9mLWNyb3Nz/LXJpdmVyLXN0YXRl/LW9mLW5pZ2VyaWEt/d2l0aC1pdHMtY2Fw/aXRhbC1pc29sYXRl/ZC1vbi13aGl0ZS1i/YWNrZ3JvdW5kLXNh/dGVsbGl0ZS1pbWFn/ZXJ5LTNkLXJlbmRl/cmluZy0yQ0JHR0s5/LmpwZw',
                    description: 'The heartbeat of Nigeria',
                },
                {
                    name: 'Abuja',
                    image: 'https://source.unsplash.com/featured/?abuja,nigeria',
                    description: 'Serenity meets elegance',
                },
                {
                    name: 'Akwa Ibom',
                    image: 'https://unsplash.com/photos/oranges-peek-through-lush-green-leaves-QGSrJHopKwY',
                    description: 'Coal city adventures',
                },
                ].map((destination, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardMedia
                        component="img"
                        height="160"
                        image={crossRiverImage}
                        alt={destination.name}
                    />
                    <CardContent sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" gutterBottom>
                        {destination.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                        {destination.description}
                        </Typography>
                    </CardContent>
                    <Box sx={{ p: 2, pt: 0 }}>
                        <Button variant="outlined" fullWidth onClick={()=> navigate('/book')}>
                        Book Now
                        </Button>
                    </Box>
                    </Card>
                </Grid>
                ))}
            </Grid>
            </Box>

            {/* WHY CHOOSE US */}
            <Box sx={{ mt: 10 }}>
            <Typography variant="h4" gutterBottom>
                Why Choose Us
            </Typography>

            <Grid container spacing={4}>
                {[
                {
                    icon: <ShieldIcon color="primary" sx={{ fontSize: 40 }} />,
                    title: 'Safe & Secure',
                    description: 'Your data and payments are protected.',
                },
                {
                    icon: <GpsFixedIcon color="primary" sx={{ fontSize: 40 }} />,
                    title: 'Live Tracking',
                    description: 'Track your journey in real time.',
                },
                {
                    icon: <AttachMoneyIcon color="primary" sx={{ fontSize: 40 }} />,
                    title: 'Best Prices',
                    description: 'No hidden fees. Honest pricing.',
                },
                {
                    icon: <HeadsetMicIcon color="primary" sx={{ fontSize: 40 }} />,
                    title: '24/7 Support',
                    description: 'We’re always here for you.',
                },
                ].map((item, i) => (
                <Grid item xs={12} sm={6} md={3} key={i}>
                    <Paper
                    elevation={3}
                    sx={{
                        p: 3,
                        textAlign: 'center',
                        height: '100%',
                        borderRadius: 2,
                        transition: '0.3s',
                        '&:hover': {
                        transform: 'scale(1.03)',
                        boxShadow: 6,
                        },
                    }}
                    >
                    <Box mb={2}>{item.icon}</Box>
                    <Typography variant="h6" gutterBottom>
                        {item.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {item.description}
                    </Typography>
                    </Paper>
                </Grid>
                ))}
            </Grid>
            </Box>


            {/* TESTIMONIALS */}
            <Box sx={{ mt: 10 }}>
            <Typography variant="h4" gutterBottom>
                What Our Travelers Say
            </Typography>

            <Grid container spacing={4}>
                {reviews.map((testimonial, i) => (
                <Grid item xs={12} sm={6} md={4} key={i}>
                    <Card elevation={3} sx={{ p: 3, height: '100%' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar src={testimonial.avatar} sx={{ mr: 2 }} />
                        <Box>
                        <Typography variant="subtitle1" fontWeight="bold">
                            {testimonial.name}
                        </Typography>
                        <Rating value={testimonial.rating} precision={0.5} readOnly />
                        </Box>
                    </Box>
                    <CardContent sx={{ px: 0 }}>
                        <Typography variant="body2" color="text.secondary">
                        {testimonial.comment}
                        </Typography>
                    </CardContent>
                    </Card>
                </Grid>
                ))}
            </Grid>
            </Box>

            {/* ABOUT US TEASER */}
            <Box sx={{ mt: 10, textAlign: 'center' }}>
            <Typography variant="h4" gutterBottom>
                Get to Know Us
            </Typography>
            <Typography
                variant="body1"
                color="text.secondary"
                sx={{ maxWidth: 600, mx: 'auto', mb: 3 }}
            >
                We’re more than just a booking platform — we're building the most
                reliable and transparent way to travel across Nigeria. Our mission is to
                connect people, places, and peace of mind.
            </Typography>
            <Button variant="contained" color="primary" href="/about">
                Learn More About Us
            </Button>
            </Box>

            {/* FAQ SECTION */}
            <Box sx={{ mt: 10 }}>
            <Typography variant="h4" gutterBottom>
                Frequently Asked Questions
            </Typography>

            {[
                {
                question: 'How do I track my booking?',
                answer:
                    'Once you book, you’ll receive a tracking ID. Use it on our tracking page or app to see live location.',
                },
                {
                question: 'Can I change or cancel my trip?',
                answer:
                    'Yes, trips can be changed or canceled up to 24 hours before departure. Conditions may apply.',
                },
                {
                question: 'Do I need an account to book?',
                answer:
                    'You can book as a guest, but having an account gives you better control over your bookings.',
                },
            ].map((faq, index) => (
                <Accordion key={index} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography fontWeight="bold">{faq.question}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography variant="body2">{faq.answer}</Typography>
                </AccordionDetails>
                </Accordion>
            ))}
            </Box>

            <ContactSupport sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}/>

            {/* NEWSLETTER SIGNUP */}
            <Box
            sx={{
                mt: 10,
                py: 6,
                px: 4,
                backgroundColor: theme.palette.mode === 'dark' ? 'grey.800' : '#f5f5f5',
                // backgroundColor: '#f5f5f5',
                textAlign: 'center',
                borderRadius: 2,
            }}
            >
            <Typography variant="h5" gutterBottom>
                Stay Updated
            </Typography>
            <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mb: 3, maxWidth: 500, mx: 'auto' }}
            >
                Subscribe to our newsletter and get the latest updates on deals, new
                destinations, and trip tips.
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
                <TextField label="Your email" variant="outlined" />
                <Button variant="contained" color="primary">
                Subscribe
                </Button>
            </Box>
            </Box>

        </Container>
    );
};

















// /* {[
//                 {
//                     name: 'Chinedu Okafor',
//                     avatar: 'https://i.pravatar.cc/150?img=16',
//                     rating: 5,
//                     comment:
//                     'Booking was seamless and the trip went great! Loved the updates.',
//                 },
//                 {
//                     name: 'Zainab Lawal',
//                     avatar: 'https://i.pravatar.cc/150?img=4',
//                     rating: 4,
//                     comment:
//                     'Affordable and efficient. Would love more flexible rescheduling options.',
//                 },
//                 {
//                     name: 'Emeka Umeh',
//                     avatar: 'https://i.pravatar.cc/150?img=7',
//                     rating: 4.5,
//                     comment:
//                     'Best service I’ve used in Nigeria. Real-time tracking was a game changer.',
//                 },
//                 ] */}