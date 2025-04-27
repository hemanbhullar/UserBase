import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1>Welcome to My Vite + React App!</h1>
      <p>Start using our app by logging in or registering.</p>
      <Link to="/login">Login</Link> | 
      <Link to="/register">Register</Link>
    </div>
  );
}

export default Home;
