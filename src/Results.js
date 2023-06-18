import React, { useState } from 'react';
import "./App.css";

const Results = () => {
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
    <div className="results-container">
      {/* <h1 className="title">Find the security score for this image</h1> */}
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
  );
};

export default Results;