import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import Results from './Results';
import Reports from './reports';


const App = () => {
  const {data, setData} = useState();

  const handleClick = async () => {
    try {
      const response = await fetch('/api/run_model');
      if (response.ok) {
        // The Streamlit app has finished running, and the index.html is returned
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
      }
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="results" element={<Results/>} />
          <Route path="reports" element={<Reports/>} />
        </Routes>
      </div>
      <div>
      <button onClick={handleClick}>Run Streamlit App</button>
    </div>
    </Router>
  );
  
};

export default App;
