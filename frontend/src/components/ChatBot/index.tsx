import React, { useState } from 'react';
import api from '../../utils/api';
import styles from './styles.module.css';

export default function ChatBot() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setResponse('');

    try {
      const result = await api.chat(question);
      setResponse(result.answer || JSON.stringify(result));
    } catch (err) {
      setError('Failed to get response from AI. Is the backend running?');
      console.error('Chat error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <h2>🤖 AI Chat Assistant</h2>
      <p>Ask questions about Physical AI and Humanoid Robotics!</p>

      <form onSubmit={handleSubmit} className={styles.chatForm}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about physical AI..."
          rows={4}
          className={styles.textarea}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className={styles.submitButton}
        >
          {loading ? 'Thinking...' : 'Ask AI'}
        </button>
      </form>

      {error && (
        <div className={styles.error}>
          ⚠️ {error}
        </div>
      )}

      {response && (
        <div className={styles.response}>
          <h3>AI Response:</h3>
          <div className={styles.responseText}>
            {response}
          </div>
        </div>
      )}

      {loading && (
        <div className={styles.loading}>
          <p>AI is thinking...</p>
        </div>
      )}
    </div>
  );
}
