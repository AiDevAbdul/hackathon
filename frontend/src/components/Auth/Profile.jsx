import React, { useState, useEffect } from 'react';
import AuthService from '../../services/authService';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      setIsLoading(true);
      const userData = await AuthService.getCurrentUser();
      setUser(userData);
    } catch (err) {
      setError('Failed to load user profile. Please log in again.');
      console.error('Profile load error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    AuthService.logout();
    window.location.href = '/'; // Redirect to home page
  };

  if (isLoading) {
    return <div className="profile">Loading profile...</div>;
  }

  if (error) {
    return <div className="profile error">{error}</div>;
  }

  if (!user) {
    return <div className="profile">Not logged in</div>;
  }

  return (
    <div className="profile">
      <h2>User Profile</h2>
      <div className="profile-details">
        <div className="profile-field">
          <strong>Name:</strong> {user.name}
        </div>
        <div className="profile-field">
          <strong>Email:</strong> {user.email}
        </div>
        <div className="profile-field">
          <strong>Role:</strong> {user.role}
        </div>
        {user.background_software && (
          <div className="profile-field">
            <strong>Software Background:</strong> {user.background_software}
          </div>
        )}
        {user.background_hardware && (
          <div className="profile-field">
            <strong>Hardware Background:</strong> {user.background_hardware}
          </div>
        )}
      </div>
      <div className="profile-actions">
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>
    </div>
  );
};

export default Profile;