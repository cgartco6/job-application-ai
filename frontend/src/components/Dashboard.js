import React, { useState } from 'react';
import { uploadCV } from '../services/api';

const CVUpload = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Check file type and size
      const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 
                         'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      
      if (!validTypes.includes(selectedFile.type)) {
        setError('Invalid file type. Please upload PDF, DOCX, JPG, or PNG.');
        return;
      }
      
      if (selectedFile.size > 5 * 1024 * 1024) { // 5MB
        setError('File size too large. Maximum size is 5MB.');
        return;
      }
      
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }
    
    setIsProcessing(true);
    setError('');
    
    try {
      const result = await uploadCV(file);
      onUpload(result);
    } catch (err) {
      setError('Upload failed. Please try again.');
      console.error('CV upload error:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="cv-upload">
      <h2>Upload Your CV</h2>
      <p>Supported formats: PDF, DOCX, JPG, PNG (max 5MB)</p>
      
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <label className="file-input-label">
            Choose File
            <input 
              type="file" 
              accept=".pdf,.docx,.jpg,.jpeg,.png" 
              onChange={handleFileChange} 
              className="file-input" 
            />
          </label>
          {file && <span className="file-name">{file.name}</span>}
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button 
          type="submit" 
          disabled={!file || isProcessing}
          className="submit-button"
        >
          {isProcessing ? 'Processing...' : 'Upload & Process'}
        </button>
      </form>
    </div>
  );
};

export default CVUpload;
