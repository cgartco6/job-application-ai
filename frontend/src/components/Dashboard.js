import React, { useState } from 'react';
import CVUpload from './CVUpload';
import JobList from './JobList';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  
  const handleCVUpload = (cvData) => {
    // Process CV data and set user state
    setUser(cvData);
  };

  return (
    <div>
      <h1>Job Application AI</h1>
      {!user ? (
        <CVUpload onUpload={handleCVUpload} />
      ) : (
        <JobList user={user} />
      )}
    </div>
  );
};

export default Dashboard;
