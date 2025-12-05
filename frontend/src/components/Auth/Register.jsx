import React, { useState } from 'react';
import AuthService from '../../services/authService';

const Register = ({ onRegisterSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    background_software: '',
    background_hardware: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await AuthService.register(formData);
      if (onRegisterSuccess) {
        onRegisterSuccess();
      }
    } catch (err) {
      setError('Registration failed. Please check your information and try again.');
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-form register-form">
      <h2>Create Account</h2>
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength="8"
          />
        </div>

        <div className="form-group">
          <label htmlFor="background_software">Software Background (Optional):</label>
          <input
            type="text"
            id="background_software"
            name="background_software"
            value={formData.background_software}
            onChange={handleChange}
            placeholder="e.g., Python, JavaScript, C++"
          />
        </div>

        <div className="form-group">
          <label htmlFor="background_hardware">Hardware Background (Optional):</label>
          <input
            type="text"
            id="background_hardware"
            name="background_hardware"
            value={formData.background_hardware}
            onChange={handleChange}
            placeholder="e.g., Arduino, Raspberry Pi, ROS"
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Creating Account...' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default Register;