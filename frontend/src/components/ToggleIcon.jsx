import { useThemeMode } from '../contexts/ThemeContext';
import { IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { useTheme } from '@mui/material/styles';

function ThemeToggle() {
  const { mode, toggleColorMode } = useThemeMode();
  const theme = useTheme();

  return (
    <IconButton onClick={toggleColorMode} color="inherit">
      {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
    </IconButton>
  );
}

export { ThemeToggle };

