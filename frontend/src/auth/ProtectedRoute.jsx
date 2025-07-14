import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';


export default function ProtectedRoute({ path, children }) {
  const { isLoggedIn } = useAuth();
  const pathLink = `/login?next=${path}`;
  return isLoggedIn ? children : <Navigate to={pathLink} />;
}

