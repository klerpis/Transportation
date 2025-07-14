import { Link } from 'react-router-dom';

import { Box, Drawer, List, ListItem, ListItemIcon, // Switch, 
    ListItemButton, ListItemText} from '@mui/material';
    
// import SettingsIcon from '@mui/icons-material/Settings';
// import DoorBackIcon from '@mui/icons-material/DoorBack';
// import { ExpandLess, ExpandMore } from '@mui/icons-material';
// import Collapse from '@mui/material/Collapse';
// import { Button, Divider } from '@mui/material';



const Sidebar = ({ drawerOpen, setDrawerOpen, isLoggedIn, 
                    location, navLinks, theme, handleLogout, 
                    openSubMenu, setOpenSubMenu}) => { 
        
        // const navLinks = [
        //     { text: 'Home', path: '/', icon: <HomeIcon />, mustLogIn: false },
        //     { text: 'About', path: '/about', icon: <InfoIcon />, mustLogIn: false },
        //     { text: 'Login', path: '/login', icon: <ReceiptIcon />, mustLogIn: false },
        //     { text: 'Booking Confirmation', path: '/book/confirmed', icon: <ReceiptIcon />, mustLogIn: false },
        //     { text: 'Sign Up', path: '/register', icon: <ReceiptIcon />, mustLogIn: false },
        //     { text: 'Live Journey', path: '/live', icon: <MapIcon />, mustLogIn: true },
        //     { text: 'Bookings', path: '/bookings', icon: <ReceiptIcon />, mustLogIn: true },
        //     { text: 'Profile', path: '/profile', icon: <PersonIcon />, mustLogIn: true },    
        //     { text: 'Review', path: '/reviews', icon: <PersonIcon />, mustLogIn: true },    
        //     { text: 'History', path: '/payments/history', icon: <PersonIcon />, mustLogIn: true },    
        //     // { text: 'Logout', path: '/', icon: <ReceiptIcon />, mustLogIn: true },
        // ];
        return (
                <Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
                    <Box sx={{ width: 250 }}>
                        <List>
                            {navLinks.map((link, index) => {
                                let item = <></>
                                    if (!isLoggedIn) {
                                        item = link.mustLogIn ? <></>
                                        : 
                                        item = <ListItem disablePadding>
                                                    <ListItemButton component={Link} to={link.path}
                                                    onClick={() => setDrawerOpen(false)}
                                                    sx={{'&.Mui-selected': {
                                                        backgroundColor: theme.palette.action.selected,
                                                    },}}
                                                    >
                                                        <ListItemIcon>{link.icon}</ListItemIcon>
                                                        <ListItemText primary={link.text} />
                                                    </ListItemButton>
                                                </ListItem>
                                        
                                        // <Button color='inherit' component={Link} to={link.path}> {link.text} </Button>

                                        
                                    }  else if ((isLoggedIn) && (link.text === 'Login'))  {
                                        item = <></>
                                    }   else if (!isLoggedIn && link.text === 'Sign Up') {
                                        // item = <Button color='inherit' component={Link} to={link.path}> {link.text} </Button> 

                                        item = <ListItem disablePadding>
                                                    <ListItemButton component={Link} to={link.path}>
                                                        <ListItemIcon>{link.icon}</ListItemIcon>
                                                        <ListItemText primary={link.text} />
                                                    </ListItemButton>
                                                </ListItem>
                                        
                                    }   else if (isLoggedIn && link.text === 'Sign Up') {
                                        item = <></>
                                        
                                    } else {
                                        // item = <Button color='inherit' component={Link} to={link.path}> {link.text} </Button> 

                                        item = <ListItem disablePadding>
                                                    <ListItemButton component={Link} to={link.path}
                                                    onClick={() => setDrawerOpen(false)}
                                                    sx={{'&.Mui-selected': {
                                                        backgroundColor: theme.palette.action.selected,
                                                    },}}
                                                    >
                                                        <ListItemIcon>{link.icon}</ListItemIcon>
                                                        <ListItemText primary={link.text} />
                                                    </ListItemButton>
                                                </ListItem>

                                    }
                                    return item
                                })
                            }


{/* 
                            {isLoggedIn ? (<> 
                                {navLinks.map((link, index) => {

                                 return(
                                    <ListItem key={index} disablePadding>
                                        <ListItemButton
                                            component={Link}
                                            to={link.path}
                                            selected={location.pathname === link.path}
                                            onClick={() => setDrawerOpen(false)}
                                            sx={{
                                            '&.Mui-selected': {
                                                backgroundColor: theme.palette.action.selected,
                                            },}}>
                                                <ListItemIcon>{link.icon}</ListItemIcon>
                                                <ListItemText primary={link.text} />
                                        </ListItemButton>
                                    </ListItem>
                                )
                            }
                            )}

                    



                                 LOGOUT SIDEBAR 
                                <ListItem disablePadding>
                                    <ListItemButton onClick={() => console.log('logout')}>
                                        <ListItemIcon><DoorBackIcon /></ListItemIcon>
                                        <ListItemText primary="Logout" />
                                    </ListItemButton>
                                </ListItem>                
                            
                            </>) : (<> 

                                {/* LOGIN SIDEBAR \*}
                                <ListItem disablePadding>
                                    <ListItemButton component={Link} to="/login">
                                        <ListItemText primary="Login" />
                                    </ListItemButton>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemButton component={Link} to="/register">
                                        <ListItemText primary="Sign Up" />
                                    </ListItemButton>
                                </ListItem>
                            </>)}


                                <ListItem disablePadding>
                                    <ListItemButton onClick={() => setOpenSubMenu(!openSubMenu)}>
                                        <ListItemIcon><SettingsIcon /></ListItemIcon>
                                        <ListItemText primary="Settings" />
                                        {openSubMenu ? <ExpandLess /> : <ExpandMore />}
                                    </ListItemButton>
                                </ListItem>
                                <Collapse in={openSubMenu} timeout="auto" unmountOnExit>
                                    <List component="div" disablePadding>
                                        <ListItemButton sx={{ pl: 4 }} component={Link} to="/profile">
                                            <ListItemText primary="Profile" />
                                        </ListItemButton>
                                        <ListItemButton sx={{ pl: 4 }} component={Link} to="/security">
                                            <ListItemText primary="Security" />
                                        </ListItemButton>
                                    </List>
                                </Collapse> */}

                        </List>
                    </Box>
                </Drawer>
            );
            };

export default Sidebar;