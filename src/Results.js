import React, { useState } from 'react';
import "./App.css";

const Results = () => {

  //adds uploaded image to image-contaiber
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      setUploadedImage(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };



  return (
    <div className="container">
      <div className="left-section">
        <div className="image-container">
          {uploadedImage ? (
            <img className="uploaded-image" src={uploadedImage} alt="Uploaded" />
          ) : (
            <img className="uploaded-image" src="uploading-img.png" alt="Uploading" />
          )}
        </div>
        <div className="upload-container">
          <input type="file" onChange={handleImageUpload} className="upload-button" accept="image/*" />
        </div>
      </div>

      <div className="right-section">
        <p className="subtitle">Using our (describe the model), we will find the closet match to your hotel room and let you know if it has been flagged for human trafficking.</p>  
        <p className="subtitle">Upload an image to begin.</p>  
      </div>
    </div>
  );
};

export default Results;