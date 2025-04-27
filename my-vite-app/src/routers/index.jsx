import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../views/Home.jsx';
import Login from '../views/Login.jsx';
import Register from '../views/Register.jsx';
import Dashboard from '../views/Dashboard.jsx';  // Protected route

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;
