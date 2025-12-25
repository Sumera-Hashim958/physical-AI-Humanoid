import React, { useState } from 'react';
import api from '../../utils/api';
import styles from './styles.module.css';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (token: string, user: any) => void;
}

export default function AuthModal({ isOpen, onClose, onSuccess }: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'login') {
        const response = await api.login(email, password);
        if (response.access_token) {
          localStorage.setItem('token', response.access_token);
          localStorage.setItem('user', JSON.stringify({ email }));
          onSuccess(response.access_token, { email });
          onClose();
        } else {
          setError(response.detail || 'Login failed');
        }
      } else {
        const response = await api.register(email, password, fullName);
        if (response.email) {
          // Auto-login after register
          const loginResp = await api.login(email, password);
          if (loginResp.access_token) {
            localStorage.setItem('token', loginResp.access_token);
            localStorage.setItem('user', JSON.stringify(response));
            onSuccess(loginResp.access_token, response);
            onClose();
          }
        } else {
          setError(response.detail || 'Registration failed');
        }
      }
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeBtn} onClick={onClose}>×</button>
        
        <h2>{mode === 'login' ? 'Login' : 'Register'}</h2>
        
        <form onSubmit={handleSubmit}>
          {mode === 'register' && (
            <div className={styles.formGroup}>
              <label>Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                placeholder="Enter your full name"
              />
            </div>
          )}
          
          <div className={styles.formGroup}>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>
          
          <div className={styles.formGroup}>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
              minLength={6}
            />
          </div>
          
          {error && <div className={styles.error}>{error}</div>}
          
          <button type="submit" className={styles.submitBtn} disabled={loading}>
            {loading ? 'Please wait...' : mode === 'login' ? 'Login' : 'Register'}
          </button>
        </form>
        
        <div className={styles.switchMode}>
          {mode === 'login' ? (
            <p>
              Don't have an account?{' '}
              <button onClick={() => setMode('register')}>Register</button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button onClick={() => setMode('login')}>Login</button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
