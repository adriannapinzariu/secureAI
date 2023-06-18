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


    // Perform any additional actions with the stored data,  generating a report
    const filename = 'report1.pdf';
    const repoUrl = 'https://github.com/adriannapinzariu/secureAI';
    const fileUrl = `${repoUrl}/raw/main/public/${filename}`;

  // Create a temporary anchor element
  const a = document.createElement('a');
  a.href = fileUrl;
  a.download = filename;

   // Fetch the report file from the GitHub repository
   fetch('https://api.github.com/repos/adriannapinzariu/secureAI/contents/public/report1.pdf')
   .then((response) => response.json())
   .then((data) => {
     // Extract the download URL from the API response
     const downloadUrl = data.download_url;
     if (downloadUrl) {
       // Create a temporary anchor element
       const a = document.createElement('a');
       a.href = downloadUrl;
       a.download = 'report1.pdf';

       // Programmatically trigger the download
       a.click();
     } else {
       console.log('Failed to fetch download URL.');
     }
   })
   .catch((error) => {
     console.log('An error occurred while fetching the file:', error);
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
    </div>
  );
};


export default Reports;