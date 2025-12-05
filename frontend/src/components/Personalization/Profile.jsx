import React, { useState, useEffect } from 'react';
import UserPreferencesService from '../../services/userPreferencesService';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    content_level_preference: '',
    example_preference: '',
    detail_preference: '',
    learning_path: []
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setIsLoading(true);
      const profileData = await UserPreferencesService.getPersonalizationProfile();
      setProfile(profileData);
      setFormData({
        content_level_preference: profileData.content_level_preference || '',
        example_preference: profileData.example_preference || '',
        detail_preference: profileData.detail_preference || '',
        learning_path: profileData.learning_path || []
      });
    } catch (err) {
      setError('Failed to load profile. Please try again.');
      console.error('Profile load error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const updatedProfile = await UserPreferencesService.updatePersonalizationProfile(formData);
      setProfile(updatedProfile);
      setIsEditing(false);
    } catch (err) {
      setError('Failed to update profile. Please try again.');
      console.error('Profile update error:', err);
    }
  };

  if (isLoading) {
    return <div className="profile">Loading profile...</div>;
  }

  if (error) {
    return <div className="profile error">{error}</div>;
  }

  return (
    <div className="profile">
      <h3>Personalization Profile</h3>

      {isEditing ? (
        <form onSubmit={handleSubmit} className="profile-edit-form">
          <div className="form-group">
            <label htmlFor="content_level_preference">Content Level Preference:</label>
            <select
              id="content_level_preference"
              name="content_level_preference"
              value={formData.content_level_preference}
              onChange={handleInputChange}
            >
              <option value="">Select level</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="example_preference">Example Preference:</label>
            <select
              id="example_preference"
              name="example_preference"
              value={formData.example_preference}
              onChange={handleInputChange}
            >
              <option value="">Select preference</option>
              <option value="theoretical">Theoretical</option>
              <option value="practical">Practical</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="detail_preference">Detail Preference:</label>
            <select
              id="detail_preference"
              name="detail_preference"
              value={formData.detail_preference}
              onChange={handleInputChange}
            >
              <option value="">Select preference</option>
              <option value="concise">Concise</option>
              <option value="detailed">Detailed</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="submit">Save</button>
            <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
          </div>
        </form>
      ) : (
        <div className="profile-display">
          <div className="profile-field">
            <strong>Content Level:</strong> {profile.content_level_preference || 'Not set'}
          </div>
          <div className="profile-field">
            <strong>Example Preference:</strong> {profile.example_preference || 'Not set'}
          </div>
          <div className="profile-field">
            <strong>Detail Preference:</strong> {profile.detail_preference || 'Not set'}
          </div>
          <button onClick={() => setIsEditing(true)} className="edit-profile-button">
            Edit Profile
          </button>
        </div>
      )}
    </div>
  );
};

export default Profile;