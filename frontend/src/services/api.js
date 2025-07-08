const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const uploadCV = async (file) => {
  const formData = new FormData();
  formData.append('cv', file);
  
  try {
    const response = await fetch(`${API_BASE_URL}/upload-cv/`, {
      method: 'POST',
      credentials: 'include',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Upload failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getJobs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/`, {
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch jobs');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

export const getApplications = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/applications/`, {
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch applications');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

export const updateSettings = async (settings) => {
  try {
    const response = await fetch(`${API_BASE_URL}/settings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(settings)
    });
    
    if (!response.ok) {
      throw new Error('Failed to update settings');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
