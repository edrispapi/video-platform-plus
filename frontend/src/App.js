import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import VideoList from './components/VideoList';
import VideoPlayer from './components/VideoPlayer';
import Dashboard from './components/Dashboard';
import './styles/global.css';

function App() {
  return (
    <div className="App">
      <Header />
      <div className="main-content">
        <Sidebar />
        <div className="content-area">
          <Routes>
            <Route path="/" element={<VideoList />} />
            <Route path="/video/:id" element={<VideoPlayer />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
