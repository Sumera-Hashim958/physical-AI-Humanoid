import React, { useState } from 'react';
import api from '../../utils/api';
import styles from './styles.module.css';

export default function Personalization() {
  const [text, setText] = useState('');
  const [difficulty, setDifficulty] = useState<'beginner' | 'intermediate' | 'advanced'>('intermediate');
  const [style, setStyle] = useState<'concise' | 'detailed'>('concise');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handlePersonalize = async () => {
    if (!text.trim()) {
      alert('Please enter some text to personalize');
      return;
    }

    setLoading(true);
    setResult('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/personalize/chapter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter_id: `custom-${Date.now()}`,
          chapter_content: text
        }),
      });

      const data = await response.json();

      // Handle validation errors properly
      if (!response.ok) {
        if (data.detail && Array.isArray(data.detail)) {
          setResult('Validation error: ' + data.detail.map((e: any) => e.msg).join(', '));
        } else {
          setResult(data.detail || 'Error occurred');
        }
        return;
      }

      setResult(data.personalized_content || 'Personalization completed');
    } catch (error) {
      setResult('Failed to personalize text. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h3>📝 Content Personalization</h3>
      <p className={styles.description}>
        Adjust the difficulty and style of any textbook content to match your learning level.
      </p>

      <div className={styles.formGroup}>
        <label>Text to Personalize:</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste textbook content here..."
          rows={5}
        />
      </div>

      <div className={styles.controls}>
        <div className={styles.formGroup}>
          <label>Difficulty Level:</label>
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as any)}>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Style:</label>
          <select value={style} onChange={(e) => setStyle(e.target.value as any)}>
            <option value="concise">Concise</option>
            <option value="detailed">Detailed</option>
          </select>
        </div>
      </div>

      <button onClick={handlePersonalize} disabled={loading} className={styles.btn}>
        {loading ? 'Personalizing...' : 'Personalize Content'}
      </button>

      {result && (
        <div className={styles.result}>
          <h4>Personalized Result:</h4>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
