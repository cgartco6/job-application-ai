import React, { useState, useEffect } from 'react';
import { getApplications } from '../services/api';
import { formatDate } from '../utils';
import './styles/components.css';

const ApplicationList = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const apps = await getApplications();
        setApplications(apps);
      } catch (error) {
        console.error('Failed to fetch applications:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchApplications();
  }, []);

  const filteredApplications = applications.filter(app => {
    if (filter === 'all') return true;
    return app.status === filter.toUpperCase();
  });

  const statusClass = (status) => {
    switch (status) {
      case 'SUBMITTED': return 'submitted';
      case 'INTERVIEW': return 'interview';
      case 'OFFER_RECEIVED': return 'offer';
      case 'REJECTED': return 'rejected';
      case 'FAILED': return 'failed';
      default: return '';
    }
  };

  if (loading) {
    return <div className="loading">Loading applications...</div>;
  }

  return (
    <div className="application-list">
      <h1>Your Applications</h1>
      
      <div className="application-controls">
        <div className="filters">
          <button 
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All Applications
          </button>
          <button 
            className={filter === 'submitted' ? 'active' : ''}
            onClick={() => setFilter('submitted')}
          >
            Submitted
          </button>
          <button 
            className={filter === 'interview' ? 'active' : ''}
            onClick={() => setFilter('interview')}
          >
            Interviews
          </button>
          <button 
            className={filter === 'offer' ? 'active' : ''}
            onClick={() => setFilter('offer')}
          >
            Offers
          </button>
        </div>
      </div>
      
      <div className="applications-container">
        {filteredApplications.length === 0 ? (
          <div className="no-applications">
            <p>No applications found</p>
          </div>
        ) : (
          filteredApplications.map(app => (
            <div key={app.id} className={`application-card ${statusClass(app.status)}`}>
              <div className="application-header">
                <h3>{app.job.title}</h3>
                <span className={`status-tag ${statusClass(app.status)}`}>
                  {app.status.replace('_', ' ')}
                </span>
              </div>
              
              <div className="application-details">
                <p><strong>Company:</strong> {app.job.company}</p>
                <p><strong>Applied:</strong> {formatDate(app.applied_at)}</p>
                {app.status === 'OFFER_RECEIVED' && (
                  <p><strong>Offer Received:</strong> {formatDate(app.updated_at)}</p>
                )}
              </div>
              
              <div className="application-actions">
                <button className="view-btn">View Cover Letter</button>
                <button className="withdraw-btn">Withdraw Application</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ApplicationList;
