import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API = 'http://localhost:8000';

export default function App() {
  const [page, setPage] = useState('login');
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || 'null'));
  
  // Form states
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('technician');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [dob, setDob] = useState('');
  const [patients, setPatients] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (token) {
      loadPatients();
    }
  }, [token]);

  const loadPatients = async () => {
    try {
      const res = await axios.get(`${API}/patients/`);
      setPatients(res.data);
    } catch (err) {
      setMessage('Error loading patients');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API}/auth/register`, {
        username,
        password,
        role
      });
      setMessage(`Registered! User: ${res.data.username}`);
      setPage('login');
      setUsername('');
      setPassword('');
    } catch (err) {
      setMessage(`Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        `${API}/auth/token`,
        `username=${username}&password=${password}`,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      const tk = res.data.access_token;
      setToken(tk);
      localStorage.setItem('token', tk);
      localStorage.setItem('user', JSON.stringify({ username }));
      setUser({ username });
      setPage('dashboard');
      setMessage('Logged in!');
    } catch (err) {
      setMessage(`Login failed: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleAddPatient = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        `${API}/patients/`,
        { first_name: firstName, last_name: lastName, dob },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPatients([...patients, res.data]);
      setFirstName('');
      setLastName('');
      setDob('');
      setMessage('Patient added!');
    } catch (err) {
      setMessage(`Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setPage('login');
    setMessage('Logged out');
  };

  if (!token) {
    return (
      <div className="landing">
        <div className="container">
          <div className="card">
          <h1>LIS - Lab Information System</h1>
          {page === 'login' ? (
            <>
              <h2>Login</h2>
              <form onSubmit={handleLogin}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="submit">Login</button>
              </form>
              <p>
                Don't have an account?{' '}
                <a href="#" onClick={() => { setPage('register'); setMessage(''); }}>
                  Register
                </a>
              </p>
              {message && <p className="error">{message}</p>}
            </>
          ) : (
            <>
              <h2>Register</h2>
              <form onSubmit={handleRegister}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="technician">Technician</option>
                  <option value="admin">Admin</option>
                  <option value="doctor">Doctor</option>
                </select>
                <button type="submit">Register</button>
              </form>
              <p>
                Already have an account?{' '}
                <a href="#" onClick={() => { setPage('login'); setMessage(''); }}>
                  Login
                </a>
              </p>
              {message && <p className="error">{message}</p>}
            </>
          )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">
        <h1>LIS Dashboard</h1>
        <p>Welcome, {user?.username}!</p>
        <button onClick={handleLogout}>Logout</button>

        <h2>Add Patient</h2>
        <form onSubmit={handleAddPatient}>
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
          <input
            type="date"
            placeholder="Date of Birth"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
          />
          <button type="submit">Add Patient</button>
        </form>

        <h2>Patients</h2>
        {patients.length === 0 ? (
          <p>No patients yet.</p>
        ) : (
          <ul>
            {patients.map((p) => (
              <li key={p.id}>
                {p.first_name} {p.last_name} (DOB: {p.dob || 'N/A'})
              </li>
            ))}
          </ul>
        )}

        {message && <p className="success">{message}</p>}
      </div>
    </div>
  );
}
