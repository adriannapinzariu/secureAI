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




   // Extract the file ID from the Google Docs URL
   const fileId = "1KHygWcpdiqNOZsFbtXVia1VSkzVlPYqNrlQ2XgWMRSU";


   // Create the download URL using the file ID
   const downloadUrl = `https://docs.google.com/document/export?format=pdf&id=${fileId}`;


   // Create a temporary anchor element
   const a = document.createElement('a');
   a.href = downloadUrl;
   a.target = '_blank';
   a.rel = 'noopener noreferrer';
   a.click();




   // Reset the input fields after storing the values
   setAddress('');
   setDescription('');


 };


 return (
   <div className="reports-container">
     <div className="l-section">
       <p className="subtitle">Create a Report</p> 
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


     <div className="r-section">
       <p className="subtitle">Download via Webscrape</p> 
     </div>




   </div>
 );
};




export default Reports;

