import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import api from '@site/src/utils/api';

export default function APITest() {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [healthData, setHealthData] = useState(null);
  const [apiInfo, setApiInfo] = useState(null);

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const health = await api.healthCheck();
      setHealthData(health);

      const info = await api.getInfo();
      setApiInfo(info);

      setBackendStatus('connected');
    } catch (error) {
      console.error('Backend connection failed:', error);
      setBackendStatus('disconnected');
    }
  };

  return (
    <Layout
      title="API Testing"
      description="Test backend API connection and endpoints">
      <div className="container" style={{marginTop: '2rem', marginBottom: '2rem'}}>
        <h1>🔌 Backend API Testing</h1>

        <div style={{
          padding: '1.5rem',
          marginBottom: '2rem',
          borderRadius: '8px',
          background: backendStatus === 'connected' ? '#d4edda' :
                      backendStatus === 'disconnected' ? '#f8d7da' : '#fff3cd',
          border: `1px solid ${backendStatus === 'connected' ? '#c3e6cb' :
                                backendStatus === 'disconnected' ? '#f5c6cb' : '#ffeaa7'}`
        }}>
          <h2>Connection Status</h2>
          <p style={{fontSize: '1.2rem', margin: 0}}>
            {backendStatus === 'checking' && '⏳ Checking backend connection...'}
            {backendStatus === 'connected' && '✅ Backend Connected!'}
            {backendStatus === 'disconnected' && '❌ Backend Disconnected'}
          </p>
          <button
            onClick={checkBackend}
            style={{
              marginTop: '1rem',
              padding: '8px 16px',
              background: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Refresh Status
          </button>
        </div>

        {backendStatus === 'connected' && (
          <>
            <div style={{
              padding: '1.5rem',
              marginBottom: '2rem',
              borderRadius: '8px',
              background: '#f8f9fa',
              border: '1px solid #dee2e6'
            }}>
              <h3>Health Check Response</h3>
              <pre style={{background: '#fff', padding: '1rem', borderRadius: '4px'}}>
                {JSON.stringify(healthData, null, 2)}
              </pre>
            </div>

            <div style={{
              padding: '1.5rem',
              marginBottom: '2rem',
              borderRadius: '8px',
              background: '#f8f9fa',
              border: '1px solid #dee2e6'
            }}>
              <h3>API Info</h3>
              <pre style={{background: '#fff', padding: '1rem', borderRadius: '4px'}}>
                {JSON.stringify(apiInfo, null, 2)}
              </pre>
            </div>

            <div style={{
              padding: '1.5rem',
              borderRadius: '8px',
              background: '#e7f3ff',
              border: '1px solid #b3d9ff'
            }}>
              <h3>Available Endpoints</h3>
              <ul>
                <li><code>GET /</code> - API Info</li>
                <li><code>GET /api/health</code> - Health Check</li>
                <li><code>POST /api/auth/register</code> - User Registration</li>
                <li><code>POST /api/auth/login</code> - User Login</li>
                <li><code>POST /api/chat</code> - AI Chat (RAG)</li>
                <li><code>POST /api/personalize</code> - Personalization</li>
                <li><code>POST /api/translate</code> - Translation</li>
              </ul>
              <p><strong>Full API Documentation:</strong> <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></p>
            </div>
          </>
        )}

        {backendStatus === 'disconnected' && (
          <div style={{
            padding: '1.5rem',
            borderRadius: '8px',
            background: '#fff3cd',
            border: '1px solid #ffeaa7'
          }}>
            <h3>⚠️ Backend Not Running</h3>
            <p>Make sure the backend server is running:</p>
            <pre style={{background: '#fff', padding: '1rem', borderRadius: '4px'}}>
              cd backend{'\n'}
              python main.py
            </pre>
            <p>Backend should be running on: <code>http://localhost:8000</code></p>
          </div>
        )}
      </div>
    </Layout>
  );
}
