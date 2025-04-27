import React, { useState } from 'react';
import { register } from '../services/authServices.js';  // We'll create this service
import { useNavigate } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState(''); // Optional: if you want to set a role during registration
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
        await register(username, email, password, role);
        navigate('/login');
    } catch (error) {
        console.error('Registration failed:', error);
        alert('Registration failed');
    }
  };

  return (
    <div className="register">
      <h1>Register</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
          <label>Role:</label>
          <input type="text" value={role} onChange={(e) => setRole(e.target.value)} />
        </div>
        <button type="submit" onClick={handleRegister}>Register</button>
      </form>
    </div>
  );
}

export default Register;
