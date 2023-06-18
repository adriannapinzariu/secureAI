import React, { useState } from 'react';
import "./App.css";

const Reports = () => {
  const [address, setAddress] = useState('');
  const [description, setDescription] = useState('');

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

    // Perform any additional actions with the stored data, such as generating a report

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
    </div>
  );
};


export default Reports;