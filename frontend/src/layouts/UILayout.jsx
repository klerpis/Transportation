
import { Breadcrumbs, Link as MuiLink } from '@mui/material';
import { Outlet, Link, useLocation } from 'react-router-dom';
// import Navbar from './Navbar';
// import Sidebar from './Sidebar';
import Footer from './Footer'; 
// import { Container } from '@mui/material';

// import { ExpandLess, ExpandMore } from '@mui/icons-material';
// import Collapse from '@mui/material/Collapse';

// import { ThemeToggle } from '../components/ToggleIcon';

import Sidebar from './Sidebar'

// import { logout } from '../services/authService';

import { Tooltip, AppBar, Toolbar, Typography, Button, 
    IconButton, Box, useTheme, useMediaQuery} from '@mui/material';
    // Switch, 
    // Drawer, List, ListItem, ListItemIcon, 
    // ListItemButton, ListItemText, 
    
// import SettingsIcon from '@mui/icons-material/Settings';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import MapIcon from '@mui/icons-material/Map';
import MenuIcon from '@mui/icons-material/Menu';
import DoorBackIcon from '@mui/icons-material/DoorBackOutlined';
import ReceiptIcon from '@mui/icons-material/Receipt';
import PersonIcon from '@mui/icons-material/Person';
import RateReviewIcon from '@mui/icons-material/RateReview';
import HistoryIcon from '@mui/icons-material/History';
import BookOnlineIcon from '@mui/icons-material/HistoryEduTwoTone';
import ConfirmationIcon from '@mui/icons-material/SensorOccupiedTwoTone';

import MaterialUISwitch from '../components/MaterialUISwitch';
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

// import { useNavigate } from 'react-router-dom';

function UILayout(){
    const [drawerOpen, setDrawerOpen] = useState(false);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    // const isLoggedIn = true; // Replace with real auth state
    const { isLoggedIn, handleLogout } = useAuth();
    const [openSubMenu, setOpenSubMenu] = useState(false);
    const location = useLocation();
    const pathnames = location.pathname.split('/').filter((x) => x);
    // let navigate = useNavigate();


    console.log('isLoggedIn', isLoggedIn)
    const navLinks = [
        { text: 'Home', path: '/', icon: <HomeIcon />, mustLogIn: false },
        { text: 'About', path: '/about', icon: <InfoIcon />, mustLogIn: false },
        { text: 'Live Journey', path: '/live', icon: <MapIcon />, mustLogIn: true },
        { text: 'Booking Confirmation', path: '/book/confirmed', icon: <ConfirmationIcon />, mustLogIn: false },
        { text: 'Bookings', path: '/bookings', icon: <BookOnlineIcon />, mustLogIn: true },
        { text: 'Profile', path: '/profile', icon: <PersonIcon />, mustLogIn: true },    
        { text: 'Review', path: '/reviews', icon: <RateReviewIcon />, mustLogIn: true },    
        { text: 'History', path: '/payments/history', icon: <HistoryIcon />, mustLogIn: true },    
        { text: 'Login', path: '/login', icon: <ReceiptIcon />, mustLogIn: false },
        { text: 'Sign Up', path: '/register', icon: <ReceiptIcon />, mustLogIn: false },
        // { text: 'Logout', path: '/', icon: <ReceiptIcon />, mustLogIn: true },
        // { text: 'Logout', path: '/', icon: <ReceiptIcon />, mustLogIn: true },
    ];
  
   // const drawer = Sidebar

    const sideNavProps = { drawerOpen, setDrawerOpen, isLoggedIn, handleLogout, 
                    location, navLinks, theme, openSubMenu, setOpenSubMenu}

    return (
        <>
            <AppBar position="sticky" sx={{ mb: 3 }}>
                <Toolbar>
                {isMobile && (
                        <IconButton color="inherit" onClick={() => setDrawerOpen(true)} edge="start" sx={{ mr: 2 }}>
                            <MenuIcon />
                        </IconButton>
                )}
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    <Button color='inherit' component={Link} to='/'> AKTC Transport Corporation </Button>
                </Typography>
                {!isMobile 
                    && navLinks.map((link, index) => {
                        let item = <></>

                        if (!isLoggedIn) {
                            item = link.mustLogIn ? <></>
                            : <Button color='inherit' component={Link} to={link.path}> {link.text} </Button>
                        }  else if ((isLoggedIn) && (link.text === 'Login'))  {
                            item = <></>
                        }   else if (!isLoggedIn && link.text === 'Sign Up') {
                            item = <Button color='inherit' component={Link} to={link.path}> {link.text} </Button> 
                        }   else if (isLoggedIn && link.text === 'Sign Up') {
                            item = <></>
                            
                        } else {
                            item = <Button color='inherit' component={Link} to={link.path}> {link.text} </Button> 
                        }
                        return item
                    })
                }
                

                < MaterialUISwitch 
                    checked={theme.palette.mode === 'dark'}
                    color="default"/>
                {isLoggedIn && 
                <Tooltip title="Logout"> 
                    <IconButton color='inherit' component={Link} onClick={
                        () => {handleLogout();}
                    }><DoorBackIcon /></IconButton>
                </Tooltip>
                }
                    {/* <ThemeToggle />
                        <Switch checked={theme.palette.mode === 'dark'}
                            onChange={onToggleTheme} color="default" />  */}
                </Toolbar>
            </AppBar>

            <Breadcrumbs sx={{ my: 2 }}>
                <MuiLink component={Link} to="/" underline="hover">
                    Home
                </MuiLink>
                {pathnames.map((value, index) => {
                    const to = `/${pathnames.slice(0, index + 1).join('/')}`;
                    return (
                    <MuiLink
                        key={to}
                        component={Link}
                        to={to}
                        underline="hover"
                        color={index === pathnames.length - 1 ? 'text.primary' : 'inherit'}
                    >
                        {value.charAt(0).toUpperCase() + value.slice(1)}
                    </MuiLink>
                    );
                })}
            </Breadcrumbs>
            

            <Sidebar {...sideNavProps} />
            
            <Box component="main" sx={{ px: { xs: 2, md: 4 } }}>
                <Outlet />
            </Box>
            <Footer />


            {/* <Navbar />
            <Sidebar />
            <Container maxWidth='lg' sx={{ mt: 4 }}>
                <Outlet />
            </Container> */}

        </> 
    );
};


export default UILayout;