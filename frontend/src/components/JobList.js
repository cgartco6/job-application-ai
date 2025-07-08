import React, { useState } from 'react';
import { formatDate, truncateText } from '../utils';
import './styles/components.css';

const JobList = ({ jobs }) => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('newest');
  
  const filteredJobs = jobs
    .filter(job => {
      if (filter === 'scam') return job.is_scam;
      if (filter === 'applied') return job.applied;
      return true;
    })
    .filter(job => 
      job.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
      job.company.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      if (sortBy === 'newest') return new Date(b.posted_at) - new Date(a.posted_at);
      if (sortBy === 'oldest') return new Date(a.posted_at) - new Date(b.posted_at);
      return 0;
    });

  return (
    <div className="job-list">
      <div className="job-controls">
        <div className="filters">
          <button 
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All Jobs
          </button>
          <button 
            className={filter === 'scam' ? 'active' : ''}
            onClick={() => setFilter('scam')}
          >
            Potential Scams
          </button>
          <button 
            className={filter === 'applied' ? 'active' : ''}
            onClick={() => setFilter('applied')}
          >
            Applied
          </button>
        </div>
        
        <div className="search-sort">
          <input
            type="text"
            placeholder="Search jobs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
          </select>
        </div>
      </div>
      
      <div className="jobs-container">
        {filteredJobs.length === 0 ? (
          <div className="no-jobs">
            <p>No jobs found matching your criteria</p>
          </div>
        ) : (
          filteredJobs.map(job => (
            <div key={job.id} className={`job-card ${job.is_scam ? 'scam' : ''}`}>
              <div className="job-header">
                <h3>{job.title}</h3>
                {job.is_scam && <span className="scam-tag">POTENTIAL SCAM</span>}
                {job.applied && <span className="applied-tag">APPLIED</span>}
              </div>
              
              <div className="job-details">
                <p><strong>Company:</strong> {job.company}</p>
                <p><strong>Location:</strong> {job.location} ({job.province}, {job.country})</p>
                <p><strong>Posted:</strong> {formatDate(job.posted_at)}</p>
                <p><strong>Source:</strong> {job.source}</p>
              </div>
              
              <div className="job-description">
                <p>{truncateText(job.description, 150)}</p>
              </div>
              
              {job.is_scam && job.scam_reason && (
                <div className="scam-reason">
                  <p><strong>Scam Reason:</strong> {job.scam_reason}</p>
                </div>
              )}
              
              <div className="job-actions">
                <button className="apply-btn">
                  {job.applied ? 'Re-Apply' : 'Apply Now'}
                </button>
                <a 
                  href={job.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="view-btn"
                >
                  View Original
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default JobList;
