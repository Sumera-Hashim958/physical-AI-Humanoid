import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import ChatBot from '@site/src/components/ChatBot';
import AuthModal from '@site/src/components/Auth';
import Personalization from '@site/src/components/Personalization';
import Translation from '@site/src/components/Translation';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/chapter-01-intro-physical-ai">
            Start Learning - Chapter 1
          </Link>
        </div>
      </div>
    </header>
  );
}

const FeatureList = [
  {
    title: 'Comprehensive Coverage',
    icon: '🤖',
    description: (
      <>
        Deep dive into Physical AI fundamentals, from sensors and perception
        to advanced control systems and human-robot interaction.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    icon: '📚',
    description: (
      <>
        Engage with interactive quizzes, code examples, and real-world
        applications to reinforce your understanding.
      </>
    ),
  },
  {
    title: 'Industry-Relevant',
    icon: '⚡',
    description: (
      <>
        Learn the latest techniques and technologies used in humanoid robotics
        and embodied AI systems across industries.
      </>
    ),
  },
];

function Feature({icon, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureIcon}>{icon}</div>
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (token && savedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(savedUser));
    } else {
      // Show login modal if not authenticated
      setIsAuthOpen(true);
    }
  }, []);

  const handleAuthSuccess = (token, userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    setIsAuthOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    setIsAuthOpen(true);
  };

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An AI-Native Interactive Textbook on Physical AI and Humanoid Robotics">

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onSuccess={handleAuthSuccess}
      />

      {/* User Info Bar */}
      {isAuthenticated && user && (
        <div style={{
          background: '#25c2a0',
          color: 'white',
          padding: '0.5rem 1rem',
          textAlign: 'right',
          fontSize: '0.9rem'
        }}>
          Welcome, {user.email || user.name}!
          <button
            onClick={handleLogout}
            style={{
              marginLeft: '1rem',
              padding: '0.25rem 0.75rem',
              background: 'white',
              color: '#25c2a0',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Logout
          </button>
          <button
            onClick={() => setIsAuthOpen(true)}
            style={{
              marginLeft: '0.5rem',
              padding: '0.25rem 0.75rem',
              background: 'transparent',
              color: 'white',
              border: '1px solid white',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Login
          </button>
        </div>
      )}

      <HomepageHeader />
      <main>
        <HomepageFeatures />

        {/* Only show features if authenticated */}
        {isAuthenticated ? (
          <>
            {/* ChatBot Section */}
            <div className="container" style={{marginTop: '3rem', marginBottom: '2rem', padding: '2rem', background: '#f0f0f0', borderRadius: '8px'}}>
              <h2 style={{color: '#333'}}>🤖 AI Chat Assistant</h2>
              <p style={{color: '#666'}}>Ask questions about Physical AI and Humanoid Robotics!</p>
              <ChatBot />
            </div>

            {/* Personalization & Translation Section */}
            <div className="container" style={{marginBottom: '3rem'}}>
              <div className="row">
                <div className="col col--6" style={{padding: '1rem'}}>
                  <div style={{padding: '2rem', background: '#e8f5e9', borderRadius: '8px', height: '100%'}}>
                    <Personalization />
                  </div>
                </div>
                <div className="col col--6" style={{padding: '1rem'}}>
                  <div style={{padding: '2rem', background: '#e3f2fd', borderRadius: '8px', height: '100%'}}>
                    <Translation />
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="container" style={{marginTop: '3rem', marginBottom: '3rem', padding: '2rem', background: '#fff3cd', borderRadius: '8px', textAlign: 'center'}}>
            <h2 style={{color: '#856404'}}>🔒 Login Required</h2>
            <p style={{color: '#856404'}}>Please login to access the AI Chat Assistant and other features.</p>
            <button
              onClick={() => setIsAuthOpen(true)}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#25c2a0',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '1rem',
                fontWeight: 'bold'
              }}
            >
              Login Now
            </button>
          </div>
        )}
      </main>
    </Layout>
  );
}
