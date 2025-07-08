import React, { useEffect, useState } from 'react';
import { formatDate } from '../utils';

const JobList = ({ user }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('/api/jobs/');
        const data = await response.json();
        setJobs(data);
      } catch (error) {
        console.error('Failed to fetch jobs:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  if (loading) return <p>Loading jobs...</p>;

  return (
    <div className="job-list">
      <h2>Recommended Jobs ({jobs.length})</h2>
      <div className="jobs-container">
        {jobs.map(job => (
          <div key={job.id} className="job-card">
            <h3>{job.title}</h3>
            <p>{job.company} • {job.location}</p>
            <p className="posted-date">Posted: {formatDate(job.posted_at)}</p>
            <div className="job-actions">
              <button className="apply-btn">Auto-Apply</button>
              <button className="view-btn">View Details</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobList;
