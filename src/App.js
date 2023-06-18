import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import Results from './Results';
import Reports from './reports';


const App = () => {
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
    </Router>
  );
};

export default App;
