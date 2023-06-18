import React, { useState } from 'react';
import "./App.css";

const Reports = () => {
  const [address, setAddress] = useState('');
  const [description, setDescription] = useState('');
  const [percentage, setPercentage] = useState(null);

  const handleAddressChange = (event) => {
    setAddress(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleDownloadReport = () => {
    // Store the inputted information in variables for later use
    const addressValue = address;
    const descriptionValue = description;
    console.log(addressValue)
    console.log(descriptionValue)

    // Send a POST request to the Flask server
    fetch('http://localhost:5000/run-model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        address: addressValue,
        description: descriptionValue
      })
    })
    .then(response => response.json())
    .then(data => {
      // The model's output is in the `percentage` field of the response
      setPercentage(data.percentage);
    });

    // Reset the input fields after storing the values
    setAddress('');
    setDescription('');
  };

  return (
    <div className="reports-container">
      <div className="input-container">
        <label htmlFor="address">Address:</label>
        <input
          type="text"
          id="address"
          value={address}
          onChange={handleAddressChange}
        />
      </div>
      <div className="input-container">
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={handleDescriptionChange}
        ></textarea>
      </div>
      <div className="input-container">
        <button className="download-report-button" onClick={handleDownloadReport}>
          Download Report
        </button>
      </div>
      {percentage && <div className="percentage-container">Model output: {percentage}%</div>}
    </div>
  );
};

export default Reports;
