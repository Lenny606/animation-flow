import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SelectionProvider } from './context/SelectionContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Home from './pages/Home';
import GenerateImage from './pages/GenerateImage';
import Songs from './pages/Songs';
import PromptGeneration from './pages/PromptGeneration';
import ImageGeneration from './pages/ImageGeneration';
import MainLayout from './components/MainLayout';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { loading, isAuthenticated } = useAuth();
  
  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

function App() {
  return (
    <AuthProvider>
      <SelectionProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/home" element={<ProtectedRoute><MainLayout><Home /></MainLayout></ProtectedRoute>} />
            <Route path="/songs" element={<ProtectedRoute><MainLayout><Songs /></MainLayout></ProtectedRoute>} />
            <Route path="/prompts" element={<ProtectedRoute><MainLayout><PromptGeneration /></MainLayout></ProtectedRoute>} />
            <Route path="/image-generation" element={<ProtectedRoute><MainLayout><ImageGeneration /></MainLayout></ProtectedRoute>} />
            <Route path="/generate" element={<ProtectedRoute><MainLayout><GenerateImage /></MainLayout></ProtectedRoute>} />
            <Route path="/" element={<Navigate to="/home" replace />} />
          </Routes>
        </Router>
      </SelectionProvider>
    </AuthProvider>
  );
}

export default App;
