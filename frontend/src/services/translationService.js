// Translation service client for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class TranslationService {
  async getUrduTranslation(slug) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/content/${slug}/translate/ur`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Translation request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Translation error:', error);
      throw error;
    }
  }
}

export default new TranslationService();