import React, { useState } from 'react';
import { login } from '../services/authServices.js';  // We'll create this service
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await login(username, password);
      if (response.access_token) {
        navigate('/dashboard');
      }
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed');
    }
  };

  return (
    <div className="login">
      <h1>Login</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit" onClick={handleLogin}>Login</button>
      </form>
    </div>
  );
}

export default Login;
