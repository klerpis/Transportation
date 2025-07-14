
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';


const Navbar = () => {
    return (
        <AppBar position='static'>
            <Toolbar>
                <Typography variant='h6' sx={{flexGrow: 1}}>
                    AKTC Transport Corporation
                </Typography>
                <Button color='inherit' component={Link} to='/'> Home </Button>
                <Button color='inherit' component={Link} to='/about'> About </Button>
                <Button color='inherit' component={Link} to='/live'> Live Journey </Button>
            </Toolbar>            
        </AppBar>
    );
};


export default Navbar;