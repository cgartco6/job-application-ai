import React, { useState, useEffect } from 'react';
import { updateSettings } from '../services/api';
import { logout } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import './styles/components.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    fullName: '',
    email: '',
    phone: '',
    jobSearchActive: true,
    dailyApplicationLimit: 100,
    provinces: [],
    jobTypes: []
  });
  
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // South African provinces
  const saProvinces = [
    'Eastern Cape', 'Free State', 'Gauteng', 
    'KwaZulu-Natal', 'Limpopo', 'Mpumalanga', 
    'North West', 'Northern Cape', 'Western Cape'
  ];
  
  const jobTypes = [
    'Full-time', 'Part-time', 'Contract', 
    'Temporary', 'Internship', 'Remote'
  ];

  useEffect(() => {
    // In a real app, you'd fetch user settings from API
    const mockSettings = {
      fullName: 'John Doe',
      email: 'john@example.com',
      phone: '+27 123 456 789',
      jobSearchActive: true,
      dailyApplicationLimit: 100,
      provinces: ['Gauteng', 'Western Cape'],
      jobTypes: ['Full-time', 'Remote']
    };
    
    setSettings(mockSettings);
    setLoading(false);
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleProvinceChange = (province) => {
    setSettings(prev => {
      const newProvinces = prev.provinces.includes(province)
        ? prev.provinces.filter(p => p !== province)
        : [...prev.provinces, province];
        
      return { ...prev, provinces: newProvinces };
    });
  };

  const handleJobTypeChange = (jobType) => {
    setSettings(prev => {
      const newJobTypes = prev.jobTypes.includes(jobType)
        ? prev.jobTypes.filter(j => j !== jobType)
        : [...prev.jobTypes, jobType];
        
      return { ...prev, jobTypes: newJobTypes };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess(false);
    setError('');
    
    try {
      await updateSettings(settings);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError('Failed to update settings. Please try again.');
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading settings...</div>;
  }

  return (
    <div className="settings">
      <h1>Account Settings</h1>
      
      <form onSubmit={handleSubmit} className="settings-form">
        <div className="form-section">
          <h2>Personal Information</h2>
          
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              name="fullName"
              value={settings.fullName}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              name="email"
              value={settings.email}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Phone Number</label>
            <input
              type="tel"
              name="phone"
              value={settings.phone}
              onChange={handleChange}
            />
          </div>
        </div>
        
        <div className="form-section">
          <h2>Job Search Preferences</h2>
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="jobSearchActive"
                checked={settings.jobSearchActive}
                onChange={handleChange}
              />
              Enable Automatic Job Search
            </label>
          </div>
          
          <div className="form-group">
            <label>Daily Application Limit</label>
            <input
              type="number"
              name="dailyApplicationLimit"
              value={settings.dailyApplicationLimit}
              onChange={handleChange}
              min="1"
              max="100"
            />
            <p className="hint">Maximum number of applications per day (1-100)</p>
          </div>
          
          <div className="form-group">
            <label>Provinces</label>
            <div className="checkbox-grid">
              {saProvinces.map(province => (
                <label key={province} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={settings.provinces.includes(province)}
                    onChange={() => handleProvinceChange(province)}
                  />
                  {province}
                </label>
              ))}
            </div>
          </div>
          
          <div className="form-group">
            <label>Job Types</label>
            <div className="checkbox-grid">
              {jobTypes.map(jobType => (
                <label key={jobType} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={settings.jobTypes.includes(jobType)}
                    onChange={() => handleJobTypeChange(jobType)}
                  />
                  {jobType}
                </label>
              ))}
            </div>
          </div>
        </div>
        
        {success && <div className="success-message">Settings updated successfully!</div>}
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-actions">
          <button type="submit" className="save-btn">Save Changes</button>
          <button type="button" className="logout-btn" onClick={handleLogout}>Log Out</button>
        </div>
      </form>
    </div>
  );
};

export default Settings;
