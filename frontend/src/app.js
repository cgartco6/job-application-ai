import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Settings from './components/Settings';
import ApplicationList from './components/ApplicationList';
import AdBanner from './components/AdBanner';
import { checkAuth } from './services/auth';
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyAuth = async () => {
      try {
        const authStatus = await checkAuth();
        setIsAuthenticated(authStatus);
      } catch (error) {
        console.error('Authentication check failed:', error);
      } finally {
        setLoading(false);
      }
    };
    
    verifyAuth();
  }, []);

  if (loading) {
    return <div className="loading">Loading application...</div>;
  }

  return (
    <Router>
      <div className="app-container">
        <AdBanner />
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={
              isAuthenticated ? 
                <Dashboard /> : 
                <Navigate to="/login" replace />
            } />
            <Route path="/settings" element={
              isAuthenticated ? 
                <Settings /> : 
                <Navigate to="/login" replace />
            } />
            <Route path="/applications" element={
              isAuthenticated ? 
                <ApplicationList /> : 
                <Navigate to="/login" replace />
            } />
            <Route path="/login" element={<div>Login Page</div>} />
          </Routes>
        </main>
        
        <footer className="app-footer">
          <p>© {new Date().getFullYear()} Job Application AI. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
