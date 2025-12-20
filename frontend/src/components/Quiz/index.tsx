import React, { useState, useEffect } from 'react';
import type { QuizQuestion, QuizProps } from '../../types/quiz';
import styles from './styles.module.css';

export default function Quiz({ questions, config }: QuizProps): JSX.Element {
  // Validate questions count (5-10)
  if (questions.length < 5 || questions.length > 10) {
    throw new Error(
      `Quiz component requires 5-10 questions. Received ${questions.length} questions.`
    );
  }

  // State management
  const [displayQuestions, setDisplayQuestions] = useState<QuizQuestion[]>([]);
  const [userAnswers, setUserAnswers] = useState<Map<number, number>>(new Map());
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);

  // Shuffle questions on mount if configured
  useEffect(() => {
    if (config?.shuffle) {
      const shuffled = [...questions].sort(() => Math.random() - 0.5);
      setDisplayQuestions(shuffled);
    } else {
      setDisplayQuestions(questions);
    }
  }, [questions, config?.shuffle]);

  // Answer selection handler
  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    if (submitted) return; // Don't allow changes after submission

    const newAnswers = new Map(userAnswers);
    newAnswers.set(questionIndex, optionIndex);
    setUserAnswers(newAnswers);
  };

  // Check if all questions are answered
  const allAnswered = userAnswers.size === displayQuestions.length;

  // Submit quiz handler
  const handleSubmit = () => {
    if (!allAnswered) return;

    // Calculate score
    let correctCount = 0;
    displayQuestions.forEach((question, index) => {
      const userAnswer = userAnswers.get(index);
      if (userAnswer === question.correctAnswer) {
        correctCount++;
      }
    });

    setScore(correctCount);
    setSubmitted(true);
  };

  // Retake quiz handler
  const handleRetake = () => {
    setUserAnswers(new Map());
    setSubmitted(false);
    setScore(0);

    // Re-shuffle if configured
    if (config?.shuffle) {
      const shuffled = [...questions].sort(() => Math.random() - 0.5);
      setDisplayQuestions(shuffled);
    }
  };

  // Keyboard navigation handler
  const handleKeyPress = (
    event: React.KeyboardEvent,
    questionIndex: number,
    optionIndex: number
  ) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleAnswerSelect(questionIndex, optionIndex);
    }
  };

  const quizTitle = config?.title || 'Chapter Quiz';
  const showCorrectExplanations = config?.showCorrectExplanations ?? false;

  return (
    <div className={styles.quizContainer}>
      <h2 className={styles.quizTitle}>{quizTitle}</h2>

      {!submitted ? (
        <>
          {/* Questions */}
          {displayQuestions.map((question, qIndex) => (
            <div key={qIndex} className={styles.questionBlock}>
              <h3 className={styles.questionText}>
                {qIndex + 1}. {question.question}
              </h3>

              <div className={styles.optionsContainer} role="radiogroup" aria-labelledby={`question-${qIndex}`}>
                {question.options.map((option, oIndex) => {
                  const isSelected = userAnswers.get(qIndex) === oIndex;

                  return (
                    <div
                      key={oIndex}
                      className={`${styles.option} ${isSelected ? styles.selected : ''}`}
                      onClick={() => handleAnswerSelect(qIndex, oIndex)}
                      onKeyPress={(e) => handleKeyPress(e, qIndex, oIndex)}
                      role="radio"
                      aria-checked={isSelected}
                      tabIndex={0}
                      aria-label={`Option ${oIndex + 1}: ${option}`}
                    >
                      <span className={styles.optionLabel}>
                        {String.fromCharCode(65 + oIndex)}.
                      </span>
                      <span className={styles.optionText}>{option}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}

          {/* Submit button */}
          <button
            className={styles.submitButton}
            onClick={handleSubmit}
            disabled={!allAnswered}
            aria-label="Submit quiz"
          >
            {allAnswered ? 'Submit Quiz' : `Answer All Questions (${userAnswers.size}/${displayQuestions.length})`}
          </button>
        </>
      ) : (
        <>
          {/* Results */}
          <div className={styles.resultsContainer}>
            <div className={styles.scoreDisplay}>
              <h3>Your Score</h3>
              <div className={styles.scoreNumber}>
                {score} / {displayQuestions.length}
              </div>
              <div className={styles.scorePercentage}>
                {Math.round((score / displayQuestions.length) * 100)}%
              </div>
            </div>

            {/* Review answers */}
            {displayQuestions.map((question, qIndex) => {
              const userAnswer = userAnswers.get(qIndex);
              const isCorrect = userAnswer === question.correctAnswer;

              return (
                <div key={qIndex} className={styles.reviewBlock}>
                  <h3 className={styles.reviewQuestionText}>
                    {qIndex + 1}. {question.question}
                  </h3>

                  <div className={styles.reviewOptions}>
                    {question.options.map((option, oIndex) => {
                      const isUserAnswer = userAnswer === oIndex;
                      const isCorrectAnswer = oIndex === question.correctAnswer;

                      let optionClass = styles.reviewOption;
                      if (isCorrectAnswer) {
                        optionClass += ` ${styles.correctAnswer}`;
                      } else if (isUserAnswer && !isCorrect) {
                        optionClass += ` ${styles.incorrectAnswer}`;
                      }

                      return (
                        <div key={oIndex} className={optionClass}>
                          <span className={styles.optionLabel}>
                            {String.fromCharCode(65 + oIndex)}.
                          </span>
                          <span className={styles.optionText}>{option}</span>
                          {isCorrectAnswer && <span className={styles.checkmark}>✓</span>}
                          {isUserAnswer && !isCorrect && <span className={styles.xmark}>✗</span>}
                        </div>
                      );
                    })}
                  </div>

                  {/* Show explanation if wrong OR if config allows showing for correct */}
                  {(!isCorrect || showCorrectExplanations) && (
                    <div className={styles.explanation}>
                      <strong>Explanation:</strong> {question.explanation}
                    </div>
                  )}
                </div>
              );
            })}

            {/* Retake button */}
            <button
              className={styles.retakeButton}
              onClick={handleRetake}
              aria-label="Retake quiz"
            >
              Retake Quiz
            </button>
          </div>
        </>
      )}
    </div>
  );
}
