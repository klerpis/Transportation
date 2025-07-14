import { createContext, useMemo, useState, useContext } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme, CssBaseline } from '@mui/material';

const ThemeContext = createContext();

export function useThemeMode() {
  return useContext(ThemeContext);
}

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState(()=>{
    let bgMode = localStorage.getItem("bgMode"); 
    // ? localStorage.getItem("bgMode") : 'light'
    console.log("bgMode", bgMode)
    if (!bgMode) {
      localStorage.setItem("bgMode", 'light'); 
      bgMode = 'light'
    }
    return bgMode
  });
  
  const toggleColorMode = () => {
    setMode((prev) => {
      const changedMode = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem("bgMode", changedMode); 
      console.log("changedMode", changedMode)
      // return (prev === 'light' ? 'dark' : 'light')
      return changedMode
    });
  };

  const theme = useMemo(() => createTheme({
    palette: {
      mode,
      primary: {
        main: '#cc6607',  // orange
      },
      secondary: {
        main: '#080166',  // navy blue
      },
      background: {
        default: mode === 'light' ? '#f5f5f5' : '#121212',
        paper: mode === 'light' ? '#ffffff' : '#1e1e1e',
      },
      text: {
        primary: mode === 'light' ? '#000000' : '#ffffff',
      },
    },
    typography: {
      fontFamily: `'Inter', 'Roboto', 'Helvetica', 'Arial', sans-serif`,
      h1: { fontSize: '2.5rem', fontWeight: 600 },
      h2: { fontSize: '2rem', fontWeight: 600 },
      h3: { fontSize: '1.5rem', fontWeight: 500 },
      body1: { fontSize: '1rem' },
      button: { textTransform: 'none' },
    },
    shape: {
      borderRadius: 12,
    },
    spacing: 8,  // default spacing unit (px)
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            fontWeight: 600,
          },
        },
      },
      MuiPaper: {
        styleOverrides: {
          root: {
            borderRadius: 12,
          },
        },
      },
    }

  }), [mode]);

  return (
    <ThemeContext.Provider value={{ mode, toggleColorMode }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
}
