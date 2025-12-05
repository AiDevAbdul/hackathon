// Authentication service for the textbook platform

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  async login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('token', this.token);

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('token', this.token);

      return data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  async getCurrentUser() {
    if (!this.token) {
      return null;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // Token might be expired, clear it
        this.logout();
        return null;
      }

      return await response.json();
    } catch (error) {
      console.error('Get current user error:', error);
      this.logout(); // Clear token on error
      return null;
    }
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
  }

  isAuthenticated() {
    return !!this.token;
  }

  getToken() {
    if (!this.token) {
      this.token = localStorage.getItem('token');
    }
    return this.token;
  }

  // Session management methods
  async refreshSession() {
    if (!this.token) {
      return false;
    }

    try {
      // Attempt to get current user to validate session
      const user = await this.getCurrentUser();
      return !!user;
    } catch (error) {
      console.error('Session refresh error:', error);
      return false;
    }
  }

  async checkSessionStatus() {
    const token = this.getToken();
    if (!token) {
      return { authenticated: false, token: null };
    }

    try {
      const user = await this.getCurrentUser();
      return {
        authenticated: !!user,
        token: this.token,
        user: user
      };
    } catch (error) {
      return {
        authenticated: false,
        token: null,
        error: error.message
      };
    }
  }
}

export default new AuthService();