# Contract: Quiz Component API

**Component**: `<Quiz>`
**Type**: React Component (MDX-compatible)
**Version**: 1.0.0
**Purpose**: Interactive quiz component for chapter assessments

## Component Interface

### Import

```typescript
import Quiz from '@site/src/components/Quiz';
```

### Props

```typescript
interface QuizProps {
  questions: QuizQuestion[];
  config?: QuizConfig;
}

interface QuizQuestion {
  id: string;                    // Unique identifier (e.g., "q101")
  question: string;               // Question text (max 300 chars)
  options: string[];              // 2-4 answer choices
  correct: number;                // Index of correct answer (0-based)
  explanation: string;            // Explanation for correct answer (max 500 chars)
  difficulty?: 'easy' | 'medium' | 'hard';  // Optional difficulty level
  section?: string;               // Optional chapter section reference
}

interface QuizConfig {
  shuffle?: boolean;              // Randomize question order (default: true)
  showExplanations?: boolean;     // Show explanations after submission (default: true)
  allowRetake?: boolean;          // Allow user to retake quiz (default: true)
  passingScore?: number;          // Percentage required to pass (default: 70, optional)
}
```

## Usage Examples

### Basic Usage (Inline Data)

```mdx
---
title: "Introduction to Physical AI"
---

# Introduction to Physical AI

[... chapter content ...]

## Quiz

<Quiz questions={[
  {
    id: "q101",
    question: "What is the primary advantage of embodied AI?",
    options: [
      "Interacts with the physical world",
      "Uses more neural networks",
      "Doesn't require sensors",
      "Only works in simulation"
    ],
    correct: 0,
    explanation: "Embodied AI systems have physical bodies that can perceive and act in the real world."
  },
  {
    id: "q102",
    question: "True or False: Physical AI requires real-time processing.",
    options: ["True", "False"],
    correct: 0,
    explanation: "Physical AI must process sensor data and execute actions in real-time to respond to dynamic environments."
  }
]} />
```

### Advanced Usage (Imported Data)

```mdx
---
title: "Sensors and Perception"
---

import Quiz from '@site/src/components/Quiz';
import quizData from './quizzes/chapter-02.json';

# Sensors and Perception

[... chapter content ...]

## Quiz

<Quiz
  questions={quizData.questions}
  config={{
    shuffle: true,
    showExplanations: true,
    allowRetake: true,
    passingScore: 75
  }}
/>
```

**External Quiz Data** (`quizzes/chapter-02.json`):

```json
{
  "questions": [
    {
      "id": "q201",
      "question": "Which sensor is most commonly used for distance measurement in robotics?",
      "options": [
        "LIDAR",
        "Microphone",
        "Thermometer",
        "Accelerometer"
      ],
      "correct": 0,
      "explanation": "LIDAR (Light Detection and Ranging) uses laser pulses to measure distances accurately, making it ideal for obstacle detection and mapping.",
      "difficulty": "easy",
      "section": "2.1 Range Sensors"
    }
  ]
}
```

## Behavior Specification

### Rendering

1. **Initial State**:
   - Display all questions (or first question if pagination enabled)
   - Each question shows:
     - Question number (e.g., "Question 1 of 5")
     - Question text
     - Answer options as clickable buttons
   - "Submit Quiz" button disabled until all questions answered

2. **Question Shuffling** (if `config.shuffle = true`):
   - Randomize question order on component mount
   - Seed based on user session (consistent across refreshes unless localStorage cleared)

### Interaction Flow

1. **User selects answer**:
   - Highlight selected option (visual feedback)
   - Store selection in component state
   - Enable "Submit Quiz" button when all questions answered

2. **User submits quiz**:
   - Calculate score: `(correct_answers / total_questions) * 100`
   - Display results:
     - Score as percentage (e.g., "You scored 80% (4/5 correct)")
     - Pass/fail status if `config.passingScore` set
   - For each question:
     - ✅ Green checkmark if correct
     - ❌ Red X if incorrect
     - Show user's selected answer
     - Show correct answer (if incorrect)
     - Show explanation (if `config.showExplanations = true`)

3. **User retakes quiz** (if `config.allowRetake = true`):
   - "Retake Quiz" button appears after submission
   - Reset component state
   - Re-shuffle questions (if `config.shuffle = true`)

### Accessibility (WCAG 2.1 AA)

- **Keyboard Navigation**:
  - Tab between answer options
  - Space/Enter to select option
  - Tab to "Submit Quiz" button, Enter to submit

- **Screen Reader Support**:
  - ARIA labels for all interactive elements
  - `aria-live` region for score announcement
  - Question number announced (e.g., "Question 1 of 5: What is...")

- **Visual**:
  - High contrast mode support (buttons visible in dark mode)
  - Focus indicators (2px outline) for keyboard users
  - Touch targets ≥44px (mobile-friendly)

### Performance

- **Rendering**: Component mounts in <100ms
- **Interaction**: Answer selection feedback in <50ms
- **Submission**: Score calculation and results display in <200ms
- **Bundle Size**: Quiz component + logic <30KB (gzipped)

## Error Handling

### Validation Errors

1. **Invalid `correct` index**:
   ```
   Error: Question q101 has invalid correct index 5 (options length: 4)
   ```
   - **Handling**: Fail build (TypeScript compilation error)

2. **Missing required props**:
   ```
   Error: Quiz component requires 'questions' prop
   ```
   - **Handling**: Fail build (React prop validation error)

3. **Empty questions array**:
   ```
   Error: Quiz must have at least 1 question (received 0)
   ```
   - **Handling**: Fail build (custom validation in component)

### Runtime Errors

1. **Corrupt localStorage data**:
   - **Handling**: Reset to initial state, log warning to console

2. **User navigates away mid-quiz**:
   - **Handling**: (Optional) Save progress to localStorage, restore on return

## State Management

### Component State (React Hooks)

```typescript
interface QuizState {
  userAnswers: Map<string, number>;  // question_id → selected_option_index
  submitted: boolean;                 // Has user submitted quiz?
  score: number | null;               // Calculated score (0-100)
  shuffledQuestions: QuizQuestion[];  // Shuffled question order
}
```

### LocalStorage Schema (Optional)

**Key**: `quiz_progress_{chapter_id}_{quiz_id}`

**Value**:
```json
{
  "version": "1.0.0",
  "lastAttempt": "2025-12-17T10:30:00Z",
  "userAnswers": {
    "q101": 0,
    "q102": 1
  },
  "submitted": true,
  "score": 80
}
```

## Testing Contract

### Unit Tests

1. **Rendering**:
   - ✅ Component renders all questions
   - ✅ Options displayed in correct order (or shuffled if configured)

2. **User Interaction**:
   - ✅ Selecting answer updates state
   - ✅ Submit button enabled only when all questions answered
   - ✅ Score calculated correctly

3. **Configuration**:
   - ✅ Shuffle works when `config.shuffle = true`
   - ✅ Explanations hidden when `config.showExplanations = false`

### Integration Tests

1. **MDX Integration**:
   - ✅ Component renders correctly when embedded in chapter MDX
   - ✅ Imported JSON quiz data parsed correctly

2. **Accessibility**:
   - ✅ Keyboard navigation works (Tab, Space, Enter)
   - ✅ Screen reader announces questions and results

### Manual Tests

1. **Mobile Responsiveness**:
   - ✅ Quiz usable on iPhone SE (375px width)
   - ✅ Touch targets ≥44px
   - ✅ No horizontal scrolling

2. **Performance**:
   - ✅ Quiz interactions <500ms (SC-007)
   - ✅ Component bundle <30KB

## Constraints

1. **Question Limits** (from FR-006):
   - Minimum: 5 questions per quiz
   - Maximum: 10 questions per quiz

2. **Answer Option Limits**:
   - Minimum: 2 options (true/false)
   - Maximum: 4 options (multiple-choice)

3. **Text Length Limits**:
   - Question text: max 300 characters
   - Explanation text: max 500 characters
   - Option text: max 150 characters

4. **Performance Budget**:
   - Component load time: <100ms
   - Interaction delay: <50ms
   - Submission delay: <200ms

## Future Enhancements (Out of Scope for P1-P3)

- ⏭️ Pagination (one question at a time instead of all at once)
- ⏭️ Timer (optional time limit for quiz)
- ⏭️ Hints (progressive hints before revealing answer)
- ⏭️ Progress tracking across chapters (requires user auth)
- ⏭️ Analytics (track question difficulty based on user performance)

## Version History

- **1.0.0** (2025-12-17): Initial contract for P1-P3 features
