// import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
// import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import UILayout from './layouts/UILayout';
import { AboutPage, HomePage, LiveJourneyPage, ReviewsPage, DynamicPaymentPage,
         BookingsPage, ProfilePage, RegisterPage, LoginPage, PaymentPage, 
         PaymentHistoryPage, NotFoundPage, TripBookingPage, BookingConfirmationPage,
        } from './pages/index';

import ProtectedRoute from './auth/ProtectedRoute';
import { ThemeProvider } from './contexts/ThemeContext';

// import { useAuth } from './contexts/AuthContext';




function App() {
  console.log("APP")

  
  return (
      <ThemeProvider> {/* theme={theme}> */}
        <CssBaseline />
        <BrowserRouter>
        <Routes> 
          <Route element={ <UILayout/> }>
            <Route path = '/' element={ <HomePage/> } />
            <Route path = '/about' element={ <AboutPage/> } />
            <Route path = '/login' element={ <LoginPage/> } />
            <Route path = '/register' element={ <RegisterPage/> } />
            <Route path = "/reviews" element={<ReviewsPage />} />

            <Route path = "/live" element={<LiveJourneyPage />} />        
            <Route path="/live/:tripId" element={<LiveJourneyPage />} />
            <Route path="/book" element={<TripBookingPage />} />        
            <Route path="/book/payment" element={<PaymentPage />} />        
            <Route path="/book/confirmed" element={<BookingConfirmationPage />} />

            <Route path = "/profile" element={<ProtectedRoute path='profile'>
                                                <ProfilePage /></ProtectedRoute>} />
            {/* <Route path = "/bookings" element={<BookingsPage />}/> */}
            <Route path = "/bookings" element={<ProtectedRoute path='bookings'>
                                                <BookingsPage /></ProtectedRoute>} />

            <Route path="payments/history" element={<PaymentHistoryPage />} />
            <Route path="/pay/:method" element={<DynamicPaymentPage />} />

            {/* <Route path="payments/history" element={<ProtectedRoute path='payments/history'>
                                                      <PaymentHistoryPage /></ProtectedRoute>} /> */}

            <Route path = "*" element={<NotFoundPage />} />

          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;





// <Route path="/book" element={<ProtectedRoute path='book'>
//                               <TripBookingPage /></ProtectedRoute>} />
// <Route path="/book/payments" element={<ProtectedRoute path='book/payments'>
//                                   <PaymentPage /></ProtectedRoute>} />
// <Route path="book/payments/history" element={<ProtectedRoute path='book/payments/history'>
//                                           <PaymentHistoryPage /></ProtectedRoute>} />



  // const [mode, setMode] = useState(()=>{
  //   let bgMode = localStorage.getItem("bgMode"); 
  //   // ? localStorage.getItem("bgMode") : 'light'
  //   console.log("bgMode", bgMode)
  //   if (!bgMode) {
  //     localStorage.setItem("bgMode", 'light'); 
  //     bgMode = 'light'
  //   }
  //   return bgMode
  // });

  // const toggleTheme = () => setMode((prev) => {
  //   const changedMode = prev === 'light' ? 'dark' : 'light';
  //   localStorage.setItem("bgMode", changedMode); 
  //   console.log("changedMode", changedMode)

  //   return changedMode

  // });
  // console.log("mode", mode)

  // // const { user, setUser, isLoggedIn, setIsLoggedIn } = useAuth();

  // // const theme = useMemo(
  // //   () =>
  // //     createTheme({
  // //       palette: {
  // //         mode,
  // //         primary: { main: '#cc6607' },
  // //         secondary: { main: '#080166' },
  // //       },
  // //     }),
  // //   [mode]
  // // );
  
  