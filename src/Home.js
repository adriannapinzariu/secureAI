import React, { useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import "./App.css";
import { Outlet } from 'react-router-dom';


//Build a carousel component for the image 
const Home = () => {
  
  const navigate = useNavigate();

  const handleStartClick = () => {
    navigate('/results');
  };

  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const carouselImages = [
    "01.jpg",
    "02.jpg",
    "03.jpg",
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % carouselImages.length);
    }, 5000);

    return () => {
      clearInterval(interval);
    };
  }, [carouselImages.length]); // Include carouselImages.length in the dependency array

//Set-up 
  return (
    <div className="container">
      <div className="left-section">
        <img
           className="carousel-image"
           src={`img-gallery/${carouselImages[currentImageIndex]}`}
           alt="Carousel"
        />
      </div>
      <div className="right-section">
        <h1 className="title">SecureAI</h1>
        <p className="subtitle">Verify your surroundings with SecureAI, an advanced tool that analyzes images to detect potential signs of exploitation and aid in the identification of human trafficking cases.</p>
        <button className="start-button" onClick={handleStartClick} >Get Started</button>
        
      </div>
      <Outlet />
    </div>
  );
};

export default Home;
