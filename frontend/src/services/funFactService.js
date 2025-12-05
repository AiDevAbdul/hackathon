// Fun fact service client for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class FunFactService {
  async getFunFacts(slug) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/content/${slug}/fun-facts`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Fun facts request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Fun facts error:', error);
      throw error;
    }
  }

  async getRandomFunFact() {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      // This would be implemented with a specific endpoint in a real application
      // For now, we'll return a mock response
      return {
        id: 'mock-id',
        content_id: 'mock-content',
        title: 'Did you know?',
        description: 'This is a sample fun fact for demonstration purposes.',
        category: 'general',
        difficulty_level: 'beginner'
      };
    } catch (error) {
      console.error('Random fun fact error:', error);
      throw error;
    }
  }

  async getFunFactsByCategory(category) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      // This would be implemented with a specific endpoint in a real application
      const response = await fetch(`${API_BASE_URL}/content/fun-facts?category=${category}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Fun facts by category request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Fun facts by category error:', error);
      throw error;
    }
  }
}

export default new FunFactService();