import React, { useState, useEffect } from 'react';
import "./App.css";

const Results = () => {
  const hotelNames = ["Hotel Azure", "Grandiose Hotel", "Inn Emerald", "Ruby Suites"];
  const locations = ["New York", "San Francisco", "Miami", "Las Vegas"];

  const [uploadedImage, setUploadedImage] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);
  const [percentage, setPercentage] = useState(null);
  const [hotelName, setHotelName] = useState('');
  const [location, setLocation] = useState('');

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      setUploadedImage(reader.result);
      setImageData(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyzeImage = () => {
    fetch('/api/analyze', { // change this to the endpoint you want to call
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: imageData }) // replace this with the actual data you want to send
    })
    .then(response => response.json())
    .then(data => {
      // handle the data returned from the Flask API here
      setAnalyzed(true);
      setPercentage(data.percentage);
      setHotelName(data.hotelName);
      setLocation(data.location);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div className="container">
      <div className={`left-section ${analyzed ? 'red-background' : ''}`}>
        <div className="image-container">
          {uploadedImage ? (
            <img className="uploaded-image" src={uploadedImage} alt="Uploaded" />
          ) : (
            <img className="uploaded-image" src="uploading-img.png" alt="Uploading" />
          )}
        </div>
        <div className="upload-container">
          <input type="file" onChange={handleImageUpload} className="upload-button" accept="image/*" />
          <button className="analyze-button" onClick={handleAnalyzeImage}>{analyzed ? "Contact Law Enforcement" : "Analyze"}</button>
        </div>
      </div>

      <div className="right-section">
        {analyzed ? (
          <div>
            <p className="subtitle">Here are the Results...</p>
            <p className="subtitle"></p>
            <p className="subtitle">We found a {percentage}% match with a hotel room at {hotelName} in {location}. This room and those like it have been flagged for previously hosting human trafficking victims.</p>
            <p className="subtitle">Please proceed with caution.</p>
          </div>
        ) : (
          <div>
            <p className="subtitle">Using our (describe the model), we will find the closest match to your hotel room and let you know if it has been flagged for human trafficking.</p>
            <p className="subtitle">Upload an image to begin.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;
