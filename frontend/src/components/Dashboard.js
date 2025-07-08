import React, { useState, useEffect } from 'react';
import CVUpload from './CVUpload';
import JobList from './JobList';
import { getJobs } from '../services/api';
import { checkAuth } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import { formatDate } from '../utils';
import './styles/Dashboard.css';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cvUploaded, setCvUploaded] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const isAuthenticated = await checkAuth();
        if (!isAuthenticated) {
          navigate('/login');
          return;
        }
        
        // In a real app, you'd fetch user data from API
        const mockUser = {
          name: 'John Doe',
          email: 'john@example.com',
          cvUploaded: false,
          jobSearchActive: true,
          lastUpdated: new Date().toISOString()
        };
        
        setUser(mockUser);
        setCvUploaded(mockUser.cvUploaded);
        
        const jobsData = await getJobs();
        setJobs(jobsData);
      } catch (error) {
        console.error('Dashboard data fetch failed:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [navigate]);

  const handleCVUpload = (result) => {
    console.log('CV processed:', result);
    setCvUploaded(true);
    // Update user state with CV data
    setUser(prev => ({
      ...prev,
      cvUploaded: true,
      skills: result.skills
    }));
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Welcome, {user?.name}</h1>
        <p>Your job search is currently <strong>{user?.jobSearchActive ? 'ACTIVE' : 'PAUSED'}</strong></p>
        <p>Last updated: {user?.lastUpdated ? formatDate(user.lastUpdated) : 'N/A'}</p>
      </header>
      
      <div className="dashboard-content">
        {!cvUploaded ? (
          <div className="cv-section">
            <h2>Get Started</h2>
            <p>Upload your CV to begin your job search</p>
            <CVUpload onUpload={handleCVUpload} />
          </div>
        ) : (
          <div className="job-section">
            <div className="stats-overview">
              <div className="stat-card">
                <h3>Total Jobs Found</h3>
                <p className="stat-value">{jobs.length}</p>
              </div>
              <div className="stat-card">
                <h3>Applications Sent</h3>
                <p className="stat-value">42</p>
              </div>
              <div className="stat-card">
                <h3>Interviews</h3>
                <p className="stat-value">5</p>
              </div>
              <div className="stat-card">
                <h3>Offers</h3>
                <p className="stat-value">1</p>
              </div>
            </div>
            
            <JobList jobs={jobs} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
