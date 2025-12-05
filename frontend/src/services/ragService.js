// RAG service client for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class RAGService {
  async chat(message, contentSlug) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/rag/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message,
          content_slug: contentSlug,
          history: [] // In a real implementation, you would include conversation history
        }),
      });

      if (!response.ok) {
        throw new Error('RAG chat request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('RAG chat error:', error);
      throw error;
    }
  }

  async validateQuestion(message, contentSlug) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/rag/validate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message,
          content_slug: contentSlug
        }),
      });

      if (!response.ok) {
        throw new Error('RAG validation request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('RAG validation error:', error);
      throw error;
    }
  }
}

export default new RAGService();