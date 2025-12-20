# Quickstart: Textbook Content Generation

**Feature**: 001-textbook-generation
**Audience**: Developers implementing this feature
**Estimated Time**: 15 minutes (setup) + 2-5 days (content authoring)

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git
- Code editor (VS Code recommended)
- Basic knowledge of Markdown and React

## Step 1: Initialize Docusaurus Project (5 minutes)

### 1.1 Create Docusaurus Site

```bash
# From repository root
npx create-docusaurus@latest textbook classic --typescript

# OR if you want to initialize in the current directory
npx create-docusaurus@latest . classic --typescript
```

**What this does**:
- Creates Docusaurus project with TypeScript support
- Uses "classic" preset (includes docs, blog, pages)
- Installs dependencies (~2 minutes)

### 1.2 Verify Installation

```bash
cd textbook  # if you created in subdirectory
npm start
```

**Expected outcome**:
- Dev server starts at `http://localhost:3000`
- See Docusaurus welcome page
- Stop server with `Ctrl+C`

## Step 2: Configure Docusaurus for Textbook (5 minutes)

### 2.1 Update `docusaurus.config.js`

```javascript
// docusaurus.config.js
const math = require('remark-math');
const katex = require('rehype-katex');

module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Interactive Textbook',
  url: 'https://your-deployment-url.vercel.app',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve docs at root
          sidebarPath: require.resolve('./sidebars.js'),
          remarkPlugins: [math], // Enable math equations
          rehypePlugins: [katex],
        },
        blog: false, // Disable blog (we only need textbook)
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Chapters',
        },
        {
          href: 'https://github.com/your-repo/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
  },
};
```

### 2.2 Install Math Plugins

```bash
npm install remark-math rehype-katex
```

### 2.3 Configure Sidebar (`sidebars.js`)

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Physical AI Fundamentals',
      items: [
        'chapter-01-intro-physical-ai',
        'chapter-02-sensors-perception',
        'chapter-03-kinematics-dynamics',
        'chapter-04-motion-planning',
        'chapter-05-control-systems',
        'chapter-06-learning-adaptation',
        'chapter-07-human-robot-interaction',
        'chapter-08-real-world-applications',
      ],
    },
  ],
};
```

## Step 3: Create Custom Components (10 minutes)

### 3.1 Create Quiz Component

```bash
mkdir -p src/components/Quiz
```

**File**: `src/components/Quiz/index.tsx`

```typescript
import React, { useState } from 'react';
import styles from './styles.module.css';

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
  difficulty?: 'easy' | 'medium' | 'hard';
}

export interface QuizProps {
  questions: QuizQuestion[];
  config?: {
    shuffle?: boolean;
    showExplanations?: boolean;
    allowRetake?: boolean;
  };
}

const Quiz: React.FC<QuizProps> = ({ questions, config = {} }) => {
  const {
    shuffle = true,
    showExplanations = true,
    allowRetake = true,
  } = config;

  const [userAnswers, setUserAnswers] = useState<Map<string, number>>(new Map());
  const [submitted, setSubmitted] = useState(false);
  const [shuffledQuestions] = useState(() =>
    shuffle ? [...questions].sort(() => Math.random() - 0.5) : questions
  );

  const handleAnswerSelect = (questionId: string, optionIndex: number) => {
    if (!submitted) {
      setUserAnswers(new Map(userAnswers.set(questionId, optionIndex)));
    }
  };

  const handleSubmit = () => {
    if (userAnswers.size === questions.length) {
      setSubmitted(true);
    }
  };

  const handleRetake = () => {
    setUserAnswers(new Map());
    setSubmitted(false);
  };

  const calculateScore = () => {
    let correct = 0;
    shuffledQuestions.forEach((q) => {
      if (userAnswers.get(q.id) === q.correct) correct++;
    });
    return Math.round((correct / questions.length) * 100);
  };

  return (
    <div className={styles.quizContainer}>
      <h3>Quiz</h3>
      {shuffledQuestions.map((q, idx) => (
        <div key={q.id} className={styles.question}>
          <p className={styles.questionText}>
            <strong>Question {idx + 1}:</strong> {q.question}
          </p>
          <div className={styles.options}>
            {q.options.map((option, optIdx) => {
              const isSelected = userAnswers.get(q.id) === optIdx;
              const isCorrect = optIdx === q.correct;
              const showFeedback = submitted;

              return (
                <button
                  key={optIdx}
                  className={`${styles.option} ${
                    isSelected ? styles.selected : ''
                  } ${
                    showFeedback && isCorrect ? styles.correct : ''
                  } ${
                    showFeedback && isSelected && !isCorrect ? styles.incorrect : ''
                  }`}
                  onClick={() => handleAnswerSelect(q.id, optIdx)}
                  disabled={submitted}
                >
                  {option}
                  {showFeedback && isCorrect && ' ✓'}
                  {showFeedback && isSelected && !isCorrect && ' ✗'}
                </button>
              );
            })}
          </div>
          {submitted && showExplanations && (
            <p className={styles.explanation}>
              <strong>Explanation:</strong> {q.explanation}
            </p>
          )}
        </div>
      ))}

      {!submitted && (
        <button
          className={styles.submitButton}
          onClick={handleSubmit}
          disabled={userAnswers.size < questions.length}
        >
          Submit Quiz
        </button>
      )}

      {submitted && (
        <div className={styles.results}>
          <h4>Your Score: {calculateScore()}% ({Array.from(userAnswers.values()).filter((ans, idx) => ans === shuffledQuestions[idx].correct).length}/{questions.length} correct)</h4>
          {allowRetake && (
            <button className={styles.retakeButton} onClick={handleRetake}>
              Retake Quiz
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default Quiz;
```

**File**: `src/components/Quiz/styles.module.css`

```css
.quizContainer {
  margin: 2rem 0;
  padding: 1.5rem;
  border: 2px solid var(--ifm-color-primary);
  border-radius: 8px;
  background: var(--ifm-color-secondary-lightest);
}

.question {
  margin: 1.5rem 0;
}

.questionText {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option {
  min-height: 48px;
  padding: 12px 20px;
  text-align: left;
  border: 2px solid var(--ifm-color-emphasis-300);
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.option:hover:not(:disabled) {
  border-color: var(--ifm-color-primary);
  background: var(--ifm-color-primary-lightest);
}

.option.selected {
  border-color: var(--ifm-color-primary);
  background: var(--ifm-color-primary-lightest);
}

.option.correct {
  border-color: var(--ifm-color-success);
  background: var(--ifm-color-success-lightest);
}

.option.incorrect {
  border-color: var(--ifm-color-danger);
  background: var(--ifm-color-danger-lightest);
}

.option:disabled {
  cursor: not-allowed;
}

.explanation {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: var(--ifm-color-info-lightest);
  border-left: 4px solid var(--ifm-color-info);
  border-radius: 4px;
  font-size: 0.95rem;
}

.submitButton,
.retakeButton {
  margin-top: 1rem;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  background: var(--ifm-color-primary);
  color: white;
  cursor: pointer;
}

.submitButton:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.results {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--ifm-color-success-lightest);
  border-radius: 8px;
  text-align: center;
}
```

### 3.2 Create Summary Component

```bash
mkdir -p src/components/Summary
```

**File**: `src/components/Summary/index.tsx`

```typescript
import React from 'react';
import styles from './styles.module.css';

export interface SummaryProps {
  bullets: string[];
  title?: string;
}

const Summary: React.FC<SummaryProps> = ({ bullets, title = 'Chapter Summary' }) => {
  if (bullets.length < 3 || bullets.length > 5) {
    throw new Error(`Summary requires 3-5 bullets (received ${bullets.length})`);
  }

  return (
    <div className={styles.summaryContainer}>
      <h3 className={styles.summaryTitle}>{title}</h3>
      <ul className={styles.summaryList}>
        {bullets.map((bullet, idx) => (
          <li key={idx}>{bullet}</li>
        ))}
      </ul>
    </div>
  );
};

export default Summary;
```

**File**: `src/components/Summary/styles.module.css`

```css
.summaryContainer {
  margin: 2rem 0;
  padding: 1.5rem 2rem;
  background: var(--ifm-color-secondary-lightest);
  border-left: 4px solid var(--ifm-color-primary);
  border-radius: 8px;
}

.summaryTitle {
  color: var(--ifm-color-primary);
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.summaryList {
  margin: 0;
  padding-left: 1.5rem;
  line-height: 1.8;
}

.summaryList li {
  margin-bottom: 0.75rem;
}

@media (max-width: 768px) {
  .summaryContainer {
    padding: 1rem 1.5rem;
  }
}
```

### 3.3 Update Custom CSS (`src/css/custom.css`)

```css
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-font-size-base: 16px;
  --ifm-line-height-base: 1.6;
}

@media (max-width: 768px) {
  :root {
    --ifm-font-size-base: 14px;
  }

  pre {
    overflow-x: auto;
    max-width: 100vw;
  }

  table {
    display: block;
    overflow-x: auto;
  }
}

img {
  max-width: 100%;
  height: auto;
}

.menu__link {
  min-height: 44px;
  padding: 12px 16px;
}
```

## Step 4: Create Chapter Content (2-5 days)

### 4.1 Create First Chapter

**File**: `docs/chapter-01-intro-physical-ai.mdx`

```mdx
---
title: "Chapter 1: Introduction to Physical AI"
description: "Explore the fundamentals of embodied intelligence and physical AI systems"
sidebar_position: 1
---

import Quiz from '@site/src/components/Quiz';
import Summary from '@site/src/components/Summary';

# Chapter 1: Introduction to Physical AI

## What is Physical AI?

Physical AI represents the convergence of robotics, artificial intelligence, and embodied cognition. Unlike traditional AI systems that operate on abstract data, physical AI systems interact with the real world through sensors, actuators, and control systems.

[... continue with 1500-3000 words of content ...]

## Chapter Summary

<Summary bullets={[
  "Physical AI combines perception, reasoning, and action in embodied agents",
  "Key challenges include uncertainty, real-time constraints, and safety",
  "Applications span manufacturing, healthcare, and autonomous systems"
]} />

## Quiz

<Quiz questions={[
  {
    id: "q101",
    question: "What is the primary difference between Physical AI and traditional AI?",
    options: [
      "Physical AI operates on embodied agents in real-world environments",
      "Physical AI only uses neural networks",
      "Physical AI doesn't require sensors",
      "Physical AI is purely theoretical"
    ],
    correct: 0,
    explanation: "Physical AI focuses on embodied agents (robots) that must perceive, reason, and act in the physical world, unlike traditional AI which often operates on abstract data."
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

### 4.2 Repeat for Chapters 2-8

Create files following the same pattern:
- `docs/chapter-02-sensors-perception.mdx`
- `docs/chapter-03-kinematics-dynamics.mdx`
- `docs/chapter-04-motion-planning.mdx`
- `docs/chapter-05-control-systems.mdx`
- `docs/chapter-06-learning-adaptation.mdx`
- `docs/chapter-07-human-robot-interaction.mdx`
- `docs/chapter-08-real-world-applications.mdx`

## Step 5: Test Locally (5 minutes)

```bash
npm start
```

**Manual Testing Checklist**:
- [ ] All 8 chapters visible in sidebar
- [ ] Chapter content renders correctly
- [ ] Summaries display with 3-5 bullets
- [ ] Quizzes are interactive (select answers, submit, see score)
- [ ] Math equations render (if any added)
- [ ] Mobile responsive (test at 375px width)
- [ ] No horizontal scrolling on mobile

## Step 6: Build and Deploy (5 minutes)

### 6.1 Build for Production

```bash
npm run build
```

**Expected outcome**:
- Build completes in <60s (SC requirement)
- Output in `/build` directory
- No errors or warnings

### 6.2 Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts to link project
```

**OR** connect GitHub repository to Vercel for auto-deployment:
1. Push code to GitHub
2. Import project in Vercel dashboard
3. Auto-deploy on every push to `main`

### 6.3 Verify Deployment

- [ ] Site loads at Vercel URL
- [ ] Page load <2s on 3G (test with Lighthouse)
- [ ] All chapters accessible
- [ ] Quizzes work on deployed site

## Troubleshooting

### Build Fails with Math Plugin Error

```bash
# Reinstall math plugins
npm uninstall remark-math rehype-katex
npm install remark-math@6 rehype-katex@7
```

### Quiz Component Not Rendering

- Verify import statement: `import Quiz from '@site/src/components/Quiz';`
- Check TypeScript errors in console
- Ensure quiz data matches `QuizQuestion` interface

### Mobile Horizontal Scrolling

- Check for wide images (add `max-width: 100%`)
- Check for long code blocks (enable horizontal scroll on `<pre>`)
- Check tables (enable `overflow-x: auto`)

## Next Steps

1. **Content Authoring**: Write/generate 6-8 chapters (use AI assistance if needed)
2. **Review & Edit**: Proofread for accuracy and clarity
3. **Add Images**: Create diagrams for key concepts (optional)
4. **Performance Audit**: Run Lighthouse CI, ensure <2s loads
5. **Accessibility Audit**: Test with keyboard navigation, screen reader

## Success Metrics (from Success Criteria)

- [ ] SC-001: All 6-8 chapters accessible on deployed site
- [ ] SC-002: Page load <2s on 3G (Lighthouse score ≥90)
- [ ] SC-003: 100% of chapters have summaries (3-5 bullets)
- [ ] SC-004: 100% of chapters have quizzes (5-10 questions)
- [ ] SC-005: Mobile-readable (≥14px font, no horizontal scroll)
- [ ] SC-006: Navigate between chapters in ≤2 clicks
- [ ] SC-007: Quiz interactions <500ms
- [ ] SC-009: Bundle size <500KB gzipped

**Estimated Total Time**: 15min setup + 2-5 days content authoring = **Ready to deploy!**
