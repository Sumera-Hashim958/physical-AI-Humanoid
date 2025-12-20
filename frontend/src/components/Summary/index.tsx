import React from 'react';
import styles from './styles.module.css';

interface SummaryProps {
  bullets: string[];
  title?: string;
}

export default function Summary({ bullets, title = 'Chapter Summary' }: SummaryProps): JSX.Element {
  // Validation: bullets must be between 3 and 5
  if (bullets.length < 3 || bullets.length > 5) {
    throw new Error(
      `Summary component requires 3-5 bullet points. Received ${bullets.length} bullets.`
    );
  }

  return (
    <div className={styles.summaryContainer}>
      <h2 className={styles.summaryTitle}>{title}</h2>
      <ul className={styles.summaryList}>
        {bullets.map((bullet, index) => (
          <li key={index} className={styles.summaryItem}>
            {bullet}
          </li>
        ))}
      </ul>
    </div>
  );
}
