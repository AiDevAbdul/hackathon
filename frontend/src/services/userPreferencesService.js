// User preferences service client for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class UserPreferencesService {
  async getThemePreference() {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/preferences/theme`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Get theme preference failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Get theme preference error:', error);
      throw error;
    }
  }

  async updateThemePreference(themeMode) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/preferences/theme`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ theme_mode: themeMode }),
      });

      if (!response.ok) {
        throw new Error('Update theme preference failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Update theme preference error:', error);
      throw error;
    }
  }

  async getPersonalizationProfile() {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/preferences/personalization`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Get personalization profile failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Get personalization profile error:', error);
      throw error;
    }
  }

  async updatePersonalizationProfile(profileData) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/preferences/personalization`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        throw new Error('Update personalization profile failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Update personalization profile error:', error);
      throw error;
    }
  }
}

export default new UserPreferencesService();