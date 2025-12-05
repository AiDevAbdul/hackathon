// Personalization service client for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class PersonalizationService {
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

  async adaptContent(content, contentSlug) {
    // In a real implementation, this would call an API to adapt content
    // For now, we'll return the content as-is
    return content;
  }

  async getLearningPath() {
    const profile = await this.getPersonalizationProfile();
    return profile.learning_path || [];
  }
}

export default new PersonalizationService();