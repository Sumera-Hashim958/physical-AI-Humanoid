/**
 * Represents a single quiz question with multiple choice options
 */
export interface QuizQuestion {
  /** The question text */
  question: string;
  /** Array of possible answer options */
  options: string[];
  /** Index of the correct answer in the options array (0-based) */
  correctAnswer: number;
  /** Explanation shown after submission */
  explanation: string;
}

/**
 * Configuration options for quiz behavior
 */
export interface QuizConfig {
  /** Whether to shuffle questions on load */
  shuffle?: boolean;
  /** Whether to show explanations for correct answers */
  showCorrectExplanations?: boolean;
  /** Title of the quiz */
  title?: string;
}

/**
 * Complete quiz data structure
 */
export interface QuizData {
  /** Array of quiz questions */
  questions: QuizQuestion[];
  /** Quiz configuration options */
  config?: QuizConfig;
}

/**
 * Props for the Quiz component
 */
export interface QuizProps {
  /** Array of quiz questions (5-10 questions) */
  questions: QuizQuestion[];
  /** Optional quiz configuration */
  config?: QuizConfig;
}
