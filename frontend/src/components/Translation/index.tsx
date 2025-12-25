import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Translation() {
  const [text, setText] = useState('');
  const [targetLang, setTargetLang] = useState('ur');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    if (!text.trim()) {
      alert('Please enter some text to translate');
      return;
    }

    setLoading(true);
    setResult('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/translate/chapter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter_id: `custom-${Date.now()}`,
          chapter_content: text,
          target_language: targetLang
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

      setResult(data.translated_content || 'Translation completed');
    } catch (error) {
      setResult('Failed to translate. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h3>🌍 Content Translation</h3>
      <p className={styles.description}>
        Translate textbook content into your preferred language.
      </p>

      <div className={styles.formGroup}>
        <label>Text to Translate:</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste English textbook content here..."
          rows={5}
        />
      </div>

      <div className={styles.formGroup}>
        <label>Target Language:</label>
        <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
          <option value="ur">Urdu (اردو)</option>
          <option value="hi">Hindi (हिंदी)</option>
          <option value="ar">Arabic (العربية)</option>
          <option value="es">Spanish (Español)</option>
          <option value="fr">French (Français)</option>
        </select>
      </div>

      <button onClick={handleTranslate} disabled={loading} className={styles.btn}>
        {loading ? 'Translating...' : 'Translate Content'}
      </button>

      {result && (
        <div className={styles.result}>
          <h4>Translated Result:</h4>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
