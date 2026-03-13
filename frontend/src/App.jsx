import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import GenerateImage from './pages/GenerateImage';
import Songs from './pages/Songs';
import MainLayout from './components/MainLayout';
import './App.css';

function App() {
  const isAuthDisabled = import.meta.env.VITE_DISABLE_AUTH === 'true';

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<MainLayout><Home /></MainLayout>} />
        <Route path="/songs" element={<MainLayout><Songs /></MainLayout>} />
        <Route path="/generate" element={<MainLayout><GenerateImage /></MainLayout>} />
        <Route path="/" element={<Navigate to={isAuthDisabled ? "/home" : "/login"} replace />} />
      </Routes>
    </Router>
  );
}

export default App;
