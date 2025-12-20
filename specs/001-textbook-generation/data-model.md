# Data Model: Textbook Content Generation

**Feature**: 001-textbook-generation
**Date**: 2025-12-17
**Type**: Static Content (No Database)

## Overview

This feature uses **file-based storage** (Markdown/MDX files) with no database or backend API. All data is stored as static content in the repository and compiled at build time by Docusaurus.

## Entity Definitions

### 1. Chapter

Represents a single educational unit covering a specific Physical AI topic.

**Storage**: Individual `.md` or `.mdx` file in `/docs` directory

**Attributes**:

| Attribute | Type | Description | Validation Rules | Storage Location |
|-----------|------|-------------|------------------|------------------|
| `id` | string | Unique identifier (filename without extension) | Pattern: `chapter-##-slug` (e.g., `chapter-01-intro-physical-ai`) | Filename |
| `title` | string | Chapter display title | Max 100 chars, required | Frontmatter: `title` |
| `description` | string | Short chapter description (for SEO, preview) | Max 200 chars | Frontmatter: `description` |
| `chapter_number` | number | Ordinal position (1-8) | Range: 1-8, unique | Frontmatter: `sidebar_position` |
| `content` | markdown | Main chapter content | 1500-3000 words (SC-011), valid Markdown | File body (after frontmatter) |
| `summary` | Summary | Chapter summary object | Required (FR-005), 3-5 bullets | MDX component: `<Summary>` |
| `quiz` | Quiz | Chapter quiz object | Required (FR-006), 5-10 questions | MDX component: `<Quiz>` |
| `created_at` | date | Initial creation date | ISO 8601 format | Frontmatter: `created` (optional) |
| `updated_at` | date | Last modification date | ISO 8601 format, auto-updated by git | Frontmatter: `last_update` or git commit |
| `tags` | string[] | Topic tags (e.g., ["sensors", "perception"]) | Optional, for categorization | Frontmatter: `tags` |
| `image` | string | Chapter hero image path | Optional, relative path to `/static/img` | Frontmatter: `image` |

**Example File Structure**:

```mdx
---
title: "Introduction to Physical AI"
description: "Explore the fundamentals of embodied intelligence and physical AI systems"
sidebar_position: 1
tags: ["introduction", "overview", "physical-ai"]
image: ./img/chapter-01-hero.png
last_update:
  date: 2025-12-17
  author: AI Textbook Team
---

# Introduction to Physical AI

Physical AI represents the convergence of robotics, artificial intelligence, and embodied cognition...

[... 1500-3000 words of content ...]

## Chapter Summary

<Summary bullets={[
  "Physical AI combines perception, reasoning, and action in embodied agents",
  "Key challenges include uncertainty, real-time constraints, and safety",
  "Applications span manufacturing, healthcare, and autonomous systems"
]} />

## Quiz

<Quiz questions={[
  // ... quiz data (see Quiz entity below)
]} />
```

**Relationships**:
- **Has One** Summary (embedded)
- **Has One** Quiz (embedded)
- **Has Many** Sections (implicit via Markdown headings)

**State Transitions**: None (static content)

---

### 2. Summary

Represents a concise overview of a chapter (3-5 key bullet points).

**Storage**: MDX component props (inline in chapter file)

**Attributes**:

| Attribute | Type | Description | Validation Rules |
|-----------|------|-------------|------------------|
| `bullets` | string[] | Array of summary points | Required, 3-5 items (FR-005), each max 200 chars |

**Example**:

```tsx
<Summary bullets={[
  "Physical AI operates in real-world environments with sensory feedback",
  "Core components: perception, planning, control, learning",
  "Challenges: uncertainty, dynamics, safety, real-time constraints"
]} />
```

**Relationships**:
- **Belongs To** Chapter (1:1)

**Validation**:
- Minimum 3 bullets, maximum 5 bullets (FR-005)
- Each bullet should be a complete sentence or phrase
- Total summary length <500 words (for mobile readability)

---

### 3. Quiz

Represents a set of assessment questions for a chapter.

**Storage**: MDX component props (inline in chapter file or imported from JSON)

**Attributes**:

| Attribute | Type | Description | Validation Rules |
|-----------|------|-------------|------------------|
| `questions` | QuizQuestion[] | Array of quiz questions | Required, 5-10 items (FR-006) |
| `config` | QuizConfig (optional) | Quiz behavior settings | Optional, defaults applied |

**QuizConfig** (Optional):

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `shuffle` | boolean | `true` | Randomize question order on each load (FR-007 acceptance 4) |
| `showExplanations` | boolean | `true` | Show explanations for incorrect answers (FR-007) |
| `allowRetake` | boolean | `true` | Allow user to retake quiz |
| `passingScore` | number | `70` | Percentage required to pass (optional, for future gamification) |

**Example**:

```tsx
<Quiz
  questions={chapterQuizData}
  config={{
    shuffle: true,
    showExplanations: true,
    allowRetake: true
  }}
/>
```

**Relationships**:
- **Belongs To** Chapter (1:1)
- **Has Many** QuizQuestion (5-10 per quiz)

---

### 4. QuizQuestion

Represents a single assessment item (multiple-choice or true/false).

**Storage**: JavaScript object in MDX component props or imported JSON file

**Attributes**:

| Attribute | Type | Description | Validation Rules |
|-----------|------|-------------|------------------|
| `id` | string | Unique question identifier | Required, pattern: `q{chapter}{number}` (e.g., `q101`, `q102`) |
| `question` | string | Question text | Required, max 300 chars, clear and unambiguous |
| `options` | string[] | Answer choices | Required, 2-4 items (multiple-choice) or 2 items (true/false) |
| `correct` | number | Index of correct answer | Required, range: 0 to options.length-1 |
| `explanation` | string | Explanation for correct answer | Required (FR-007), max 500 chars, references chapter content |
| `difficulty` | string (enum) | Question difficulty level | Optional, values: `easy`, `medium`, `hard` |
| `section` | string | Chapter section this question covers | Optional, references heading text for traceability |

**Example**:

```typescript
{
  id: "q101",
  question: "What is the primary advantage of embodied AI over traditional AI systems?",
  options: [
    "Embodied AI can interact with the physical world in real-time",
    "Embodied AI uses more neural network layers",
    "Embodied AI doesn't require sensors",
    "Embodied AI only works in simulation"
  ],
  correct: 0,
  explanation: "Embodied AI systems have physical bodies (robots) that perceive and act in the real world, unlike traditional AI which operates on abstract data. This enables real-time interaction with dynamic environments (see Section 1.2: Embodiment and Interaction).",
  difficulty: "easy",
  section: "1.2 Embodiment and Interaction"
}
```

**Relationships**:
- **Belongs To** Quiz (many:1)

**Validation Rules**:
- At least 1 question per major chapter section (SC-013)
- Each chapter should have mix of difficulties (suggested: 60% easy, 30% medium, 10% hard)
- Explanations MUST reference specific chapter sections (for grounding)

---

## Data Flow

```
[Chapter Markdown Files]
       ↓
[Docusaurus Build Process]
       ↓
[Static HTML + React Hydration]
       ↓
[User Browser]
       ↓
[Quiz Component State Management]
       ↓
[LocalStorage (optional, for progress tracking)]
```

**Build Time**:
1. Docusaurus reads all `.md`/`.mdx` files from `/docs`
2. Parses frontmatter (metadata) and Markdown/MDX content
3. Transforms MDX components (`<Quiz>`, `<Summary>`) into React components
4. Generates static HTML for each chapter
5. Bundles React code for client-side interactivity (quiz state)

**Runtime** (Client-Side):
1. User navigates to chapter → static HTML loads instantly
2. React hydrates interactive components (Quiz)
3. User interacts with quiz → state managed in React hooks
4. Quiz submission → client-side validation, score calculation, feedback display
5. (Optional) Quiz progress stored in browser localStorage for retakes

---

## File-Based Schema

Since there's no database, the "schema" is enforced by:

1. **File naming convention**:
   - Pattern: `chapter-{number}-{slug}.mdx`
   - Example: `chapter-01-intro-physical-ai.mdx`

2. **Frontmatter validation** (via Docusaurus):
   - Required fields: `title`, `sidebar_position`
   - Optional fields: `description`, `tags`, `image`, `last_update`

3. **TypeScript types** (for Quiz components):

```typescript
// src/types/quiz.ts

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  section?: string;
}

export interface QuizConfig {
  shuffle?: boolean;
  showExplanations?: boolean;
  allowRetake?: boolean;
  passingScore?: number;
}

export interface QuizData {
  questions: QuizQuestion[];
  config?: QuizConfig;
}

export interface SummaryData {
  bullets: string[];
}
```

4. **JSON Schema** (for external quiz data files):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "questions": {
      "type": "array",
      "minItems": 5,
      "maxItems": 10,
      "items": {
        "type": "object",
        "required": ["id", "question", "options", "correct", "explanation"],
        "properties": {
          "id": { "type": "string", "pattern": "^q[0-9]+$" },
          "question": { "type": "string", "maxLength": 300 },
          "options": { "type": "array", "minItems": 2, "maxItems": 4 },
          "correct": { "type": "integer", "minimum": 0 },
          "explanation": { "type": "string", "maxLength": 500 },
          "difficulty": { "enum": ["easy", "medium", "hard"] },
          "section": { "type": "string" }
        }
      }
    }
  }
}
```

---

## Storage Estimates

| Entity | Count | Size per Item | Total Size |
|--------|-------|---------------|------------|
| Chapter (Markdown) | 6-8 | ~10-15 KB (text only) | ~60-120 KB |
| Chapter Images | 20-40 (avg 3-5 per chapter) | ~50-100 KB (optimized WebP) | ~1-4 MB |
| Quiz Data (embedded) | 40-80 questions | ~500 bytes per question | ~20-40 KB |
| Summary Data (embedded) | 24-40 bullets | ~100 bytes per bullet | ~2-4 KB |
| **Total Repository Size** | - | - | **~1.5-5 MB** (raw Markdown + images) |

**Build Output Size** (Vercel deployment):
- Static HTML: ~200-400 KB (all chapters)
- JavaScript bundles: ~150-300 KB (React + components, gzipped)
- CSS: ~30-50 KB (custom styles, gzipped)
- Images: ~1-4 MB (served via CDN, lazy loaded)

**Total Bundle** (per chapter page load):
- First load: ~300-500 KB (HTML + JS + CSS + hero image)
- Subsequent chapters: ~50-100 KB (cached JS/CSS, only HTML + new images)

**Compliance**: Meets SC-009 (<500KB bundle size) ✅

---

## Data Integrity and Validation

### Build-Time Validation

1. **Frontmatter Validation**:
   - Docusaurus validates required fields (`title`, `sidebar_position`)
   - Fails build if frontmatter is malformed

2. **TypeScript Type Checking**:
   - Quiz component props validated against `QuizData` interface
   - Fails build if quiz data doesn't match schema

3. **Content Linting** (optional, future):
   - Use `markdownlint` to enforce consistent Markdown style
   - Use `alex` to check for insensitive language

### Runtime Validation

1. **Quiz State Validation**:
   - Ensure user selects answer before submission (FR-015 edge case)
   - Validate `correct` index is within `options` array bounds

2. **LocalStorage Validation** (if implemented):
   - Validate stored quiz progress schema before loading
   - Handle corrupt data gracefully (reset to initial state)

---

## Migration Strategy

**Current State**: No existing textbook content

**Initial Population**:
1. Create 6-8 chapter files manually or via AI generation (GPT-4, Claude)
2. Review and edit each chapter for accuracy
3. Write quiz questions (5-10 per chapter)
4. Write summaries (3-5 bullets per chapter)
5. Add images/diagrams (optional for MVP)

**Future Migrations** (for feature evolution):
- If moving to dynamic content (002-rag-chatbot), chapter Markdown remains canonical source
- If adding user authentication (003-user-auth), quiz progress moves from localStorage to Neon database
- If adding i18n (005-urdu-translation), use Docusaurus i18n plugin (keeps Markdown structure)

**Backward Compatibility**: File-based approach ensures easy migration to database if needed (Markdown → parse → store in Neon)

---

## Summary

**Key Design Decisions**:
- File-based storage (no database) for simplicity and speed (Principles III, VI)
- Frontmatter + MDX for structured content with embedded interactivity
- TypeScript types for compile-time validation
- Client-side quiz state management (no backend dependency)

**Entities**:
1. **Chapter** (8 files, ~10-15 KB each)
2. **Summary** (embedded, 3-5 bullets per chapter)
3. **Quiz** (embedded, 5-10 questions per chapter)
4. **QuizQuestion** (40-80 total, ~500 bytes each)

**Storage**: ~1.5-5 MB total (repository), <500KB per page load (deployed)

**Next Step**: Generate API contracts (MDX component interfaces) in `contracts/`
