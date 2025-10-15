import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Inbox from './pages/Inbox.jsx';
import Login from './pages/Login.jsx';
import Signup from './pages/Signup.jsx';
import ChatPage from './pages/ChatPage.jsx';

function App(){
  return (
    <BrowserRouter>
      <div style={{maxWidth:900, margin:'0 auto', padding:20}}>
        <h2>WhatsEase (fixed)</h2>
        <nav style={{marginBottom:20}}>
          <Link to="/">Inbox</Link> | <Link to="/login">Login</Link> | <Link to="/signup">Signup</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Inbox/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
          <Route path="/chat/:withEmail" element={<ChatPage/>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

createRoot(document.getElementById('root')).render(<App />);
