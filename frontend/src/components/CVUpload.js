import React, { useState } from 'react';

const CVUpload = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setIsProcessing(true);
    
    const formData = new FormData();
    formData.append('cv', file);
    
    try {
      const response = await fetch('/api/upload-cv/', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      onUpload(data);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="cv-upload">
      <h2>Upload Your CV</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf,.docx,.jpg,.png" onChange={handleFileChange} />
        <button type="submit" disabled={!file || isProcessing}>
          {isProcessing ? 'Processing...' : 'Upload & Process'}
        </button>
      </form>
    </div>
  );
};

export default CVUpload;
