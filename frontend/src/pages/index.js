import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
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
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An AI-Native Interactive Textbook on Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
