/**
 * API utility for connecting to Physical AI Textbook Backend
 */

// For local development
const API_BASE_URL = 'http://localhost:8000';

// For production, update this to your deployed backend URL
// const API_BASE_URL = 'https://your-backend-url.railway.app';

export const api = {
  /**
   * Health check
   */
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.json();
  },

  /**
   * Get API info
   */
  async getInfo() {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.json();
  },

  /**
   * Chat with RAG bot
   */
  async chat(question: string, conversationId?: string) {
    const response = await fetch(`${API_BASE_URL}/api/chat/question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question,
        conversation_id: conversationId || `chat-${Date.now()}`,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Chat request failed');
    }

    return response.json();
  },

  /**
   * User authentication
   */
  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });
    return response.json();
  },

  /**
   * Register new user
   */
  async register(email: string, password: string, fullName: string, programmingLevel: string = 'beginner', hardware: string = 'none') {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name: fullName,
        programming_level: programmingLevel,
        hardware: hardware,
      }),
    });
    return response.json();
  },

  /**
   * Get current user
   */
  async getCurrentUser(token: string) {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },
};

export default api;
