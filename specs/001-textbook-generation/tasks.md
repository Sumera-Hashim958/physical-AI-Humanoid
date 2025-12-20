# Tasks: Textbook Content Generation

**Input**: Design documents from `/specs/001-textbook-generation/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are NOT requested in the specification, so NO test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Static site project**: `docs/`, `src/`, `static/` at repository root
- All paths shown below are relative to repository root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Docusaurus project with TypeScript and required dependencies

- [x] T001 Initialize Docusaurus project with TypeScript using `npx create-docusaurus@latest . classic --typescript`
- [x] T002 Install math rendering dependencies: `npm install remark-math@6 rehype-katex@7`
- [x] T003 [P] Create directory structure: `docs/`, `src/components/`, `src/css/`, `static/img/`
- [x] T004 [P] Configure TypeScript: create `tsconfig.json` with React JSX and ES2020 target
- [x] T005 Configure Docusaurus in `docusaurus.config.js`: enable math plugins (remark-math, rehype-katex), set routeBasePath to `/`, disable blog
- [x] T006 [P] Add KaTeX stylesheet to `docusaurus.config.js` stylesheets array (CDN link with integrity hash)
- [x] T007 [P] Create `src/css/custom.css` with mobile-first CSS variables (--ifm-font-size-base: 16px desktop, 14px mobile)
- [ ] T008 [P] Create `.github/workflows/deploy.yml` for Vercel auto-deploy on push to main

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components and configuration that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Configure sidebar in `sidebars.js`: create "Physical AI Fundamentals" category with 8 chapter entries (chapter-01 through chapter-08)
- [x] T010 Update navbar in `docusaurus.config.js`: set title to "Physical AI Textbook", configure docs link and GitHub link
- [x] T011 [P] Create mobile-responsive CSS in `src/css/custom.css`: media query for max-width 768px with responsive tables, images, and code blocks
- [x] T012 [P] Set up ESLint and Prettier: create `eslint.config.js` and `.prettierrc` with TypeScript and React rules

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Core Textbook Structure (Priority: P1) 🎯 MVP

**Goal**: 6-8 chapters on Physical AI, Markdown-formatted, responsive, fast-loading (<2s on 3G)

**Independent Test**: Navigate to deployed site, verify all 8 chapters visible in sidebar, click each chapter, verify content renders with headings/paragraphs/formatting, test mobile responsiveness (375px viewport), verify Chapter 1→2 navigation <2s

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create `docs/intro.md`: homepage with textbook overview, navigation instructions, and links to chapters
- [ ] T014 [P] [US1] Create `docs/chapter-01-intro-physical-ai.mdx`: frontmatter (title, description, sidebar_position: 1) + 1500-3000 words on Introduction to Physical AI
- [ ] T015 [P] [US1] Create `docs/chapter-02-sensors-perception.mdx`: frontmatter + 1500-3000 words on Sensors and Perception
- [ ] T016 [P] [US1] Create `docs/chapter-03-kinematics-dynamics.mdx`: frontmatter + 1500-3000 words on Kinematics and Dynamics
- [ ] T017 [P] [US1] Create `docs/chapter-04-motion-planning.mdx`: frontmatter + 1500-3000 words on Motion Planning
- [ ] T018 [P] [US1] Create `docs/chapter-05-control-systems.mdx`: frontmatter + 1500-3000 words on Control Systems
- [ ] T019 [P] [US1] Create `docs/chapter-06-learning-adaptation.mdx`: frontmatter + 1500-3000 words on Learning and Adaptation
- [ ] T020 [P] [US1] Create `docs/chapter-07-human-robot-interaction.mdx`: frontmatter + 1500-3000 words on Human-Robot Interaction
- [ ] T021 [P] [US1] Create `docs/chapter-08-real-world-applications.mdx`: frontmatter + 1500-3000 words on Real-World Applications
- [ ] T022 [US1] Add math equations to chapters using KaTeX syntax (inline: `$equation$`, block: `$$equation$$`) where relevant (e.g., kinematics, dynamics, control)
- [ ] T023 [P] [US1] Add 3-5 diagrams/images per chapter to `static/img/` (sensors/, kinematics/, etc.) - use WebP format, max 100KB per image
- [ ] T024 [US1] Configure responsive images in chapters: use `![alt text](path)` with max-width: 100% CSS rule
- [ ] T025 [US1] Run `npm run build` to verify all chapters build without errors and bundle size <500KB per page
- [ ] T026 [US1] Run Lighthouse audit on local build: verify performance score ≥90, page load <2s on 3G throttling
- [ ] T027 [US1] Deploy to Vercel: connect GitHub repository, configure auto-deploy, verify deployment completes in <90s

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - complete textbook with 8 chapters, responsive, performant

---

## Phase 4: User Story 2 - Chapter Summaries (Priority: P2)

**Goal**: 3-5 bullet point summaries at end of each chapter for quick revision

**Independent Test**: Navigate to any chapter, scroll to bottom, verify "Chapter Summary" section with 3-5 bullets, verify visual separation from main content, test mobile readability

### Implementation for User Story 2

- [x] T028 [US2] Create `src/components/Summary/index.tsx`: React component accepting `bullets: string[]` and `title?: string` props
- [x] T029 [US2] Create `src/components/Summary/styles.module.css`: styled box with light background, border-left accent, 1.8 line-height, mobile padding adjustments
- [x] T030 [US2] Add validation to Summary component: throw error if bullets.length < 3 or > 5
- [x] T031 [P] [US2] Add Summary component to `docs/chapter-01-intro-physical-ai.mdx`: import component, add `<Summary bullets={[...]}/>` with 3-5 key concepts
- [x] T032 [P] [US2] Add Summary component to `docs/chapter-02-sensors-perception.mdx` with 3-5 key concepts
- [x] T033 [P] [US2] Add Summary component to `docs/chapter-03-kinematics-dynamics.mdx` with 3-5 key concepts
- [x] T034 [P] [US2] Add Summary component to `docs/chapter-04-motion-planning.mdx` with 3-5 key concepts
- [x] T035 [P] [US2] Add Summary component to `docs/chapter-05-control-systems.mdx` with 3-5 key concepts
- [x] T036 [P] [US2] Add Summary component to `docs/chapter-06-learning-adaptation.mdx` with 3-5 key concepts
- [x] T037 [P] [US2] Add Summary component to `docs/chapter-07-human-robot-interaction.mdx` with 3-5 key concepts
- [ ] T038 [P] [US2] Add Summary component to `docs/chapter-08-real-world-applications.mdx` with 3-5 key concepts
- [x] T039 [US2] Verify all summaries render correctly on mobile (≥14px font, no horizontal scroll) using Chrome DevTools mobile emulation

**Checkpoint**: All chapters now have summaries; both User Story 1 AND User Story 2 work independently

---

## Phase 5: User Story 3 - Interactive Quizzes (Priority: P3)

**Goal**: 5-10 interactive quiz questions per chapter with immediate feedback and explanations

**Independent Test**: Navigate to any chapter, click "Take Quiz", answer questions, submit, verify score display, verify explanations for incorrect answers, verify retake functionality

### Implementation for User Story 3

- [x] T040 [US3] Create TypeScript types in `src/types/quiz.ts`: interfaces for `QuizQuestion`, `QuizConfig`, `QuizData`
- [x] T041 [US3] Create `src/components/Quiz/index.tsx`: React component with state management (userAnswers Map, submitted boolean, score calculation)
- [x] T042 [US3] Implement answer selection logic in Quiz component: update userAnswers Map, enable submit button when all answered
- [x] T043 [US3] Implement quiz submission logic in Quiz component: calculate score, display results with ✓/✗ indicators
- [x] T044 [US3] Implement question shuffling in Quiz component: use `Math.random()` on component mount if `config.shuffle = true`
- [x] T045 [US3] Implement retake functionality in Quiz component: reset state, re-shuffle questions
- [x] T046 [US3] Create `src/components/Quiz/styles.module.css`: button styles (min-height 48px, border-radius 8px), option states (selected, correct, incorrect), responsive mobile styles
- [x] T047 [US3] Add accessibility features to Quiz component: ARIA labels, keyboard navigation (Tab, Space/Enter), focus indicators
- [x] T048 [P] [US3] Create quiz data for Chapter 1 in `docs/chapter-01-intro-physical-ai.mdx`: 5-10 questions with options, correct answer index, explanations
- [x] T049 [P] [US3] Create quiz data for Chapter 2 in `docs/chapter-02-sensors-perception.mdx`: 5-10 questions
- [x] T050 [P] [US3] Create quiz data for Chapter 3 in `docs/chapter-03-kinematics-dynamics.mdx`: 5-10 questions
- [x] T051 [P] [US3] Create quiz data for Chapter 4 in `docs/chapter-04-motion-planning.mdx`: 5-10 questions
- [x] T052 [P] [US3] Create quiz data for Chapter 5 in `docs/chapter-05-control-systems.mdx`: 5-10 questions
- [x] T053 [P] [US3] Create quiz data for Chapter 6 in `docs/chapter-06-learning-adaptation.mdx`: 5-10 questions
- [x] T054 [P] [US3] Create quiz data for Chapter 7 in `docs/chapter-07-human-robot-interaction.mdx`: 5-10 questions
- [ ] T055 [P] [US3] Create quiz data for Chapter 8 in `docs/chapter-08-real-world-applications.mdx`: 5-10 questions
- [x] T056 [US3] Add Quiz component imports to all chapter MDX files: `import Quiz from '@site/src/components/Quiz';`
- [x] T057 [US3] Verify quiz interactions <500ms: test answer selection, submission, and results display on local dev server
- [x] T058 [US3] Verify Quiz component bundle size <30KB: run `npm run build` and check build output

**Checkpoint**: All user stories should now be independently functional (chapters + summaries + quizzes)

---

## Phase 6: User Story 4 - Content Searchability (Priority: P4)

**Goal**: Search across all chapters to find topics/concepts quickly

**Independent Test**: Type keyword (e.g., "kinematics") in search bar, verify relevant sections appear, click result, verify page scrolls to section, test "no results" message for non-existent term

### Implementation for User Story 4

- [ ] T059 [US4] Enable Docusaurus search plugin in `docusaurus.config.js`: add `@docusaurus/theme-search-algolia` OR local search plugin
- [ ] T060 [US4] Configure search index settings: include all chapter content, summaries, and headings in search index
- [ ] T061 [US4] Customize search bar placeholder text in theme config: "Search Physical AI topics..."
- [ ] T062 [US4] Test search functionality: verify keyword search returns relevant chapters, verify result highlighting, verify "no results" fallback
- [ ] T063 [US4] Verify search performance: ensure search results appear in <500ms on local build

**Checkpoint**: All 4 user stories complete and working independently

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T064 [P] Add favicon: create `static/img/favicon.ico` with Physical AI logo or robot icon
- [ ] T065 [P] Create README.md in repository root: project overview, quick start commands (`npm install`, `npm start`, `npm run build`), deployment instructions
- [ ] T066 [P] Add meta tags in `docusaurus.config.js`: SEO description, Open Graph tags for social sharing, Twitter card metadata
- [ ] T067 [P] Configure dark mode toggle in `docusaurus.config.js`: enable default Docusaurus dark mode with respect for `prefers-color-scheme`
- [ ] T068 Create 404 page in `src/pages/404.md`: custom not found page with links to homepage and chapter index
- [ ] T069 [P] Add "Back to Top" button CSS in `src/css/custom.css`: appears after scrolling >300px, smooth scroll behavior
- [ ] T070 Run final Lighthouse audit on deployed site: verify all pages score ≥90 performance, ≥95 accessibility
- [ ] T071 Run final bundle size check: verify each chapter page <500KB gzipped (JS + CSS)
- [ ] T072 Test on real mobile devices: iPhone SE (375px), Android phone, verify no horizontal scroll, tap targets ≥44px
- [ ] T073 Create quickstart validation script: verify all 8 chapters exist, all have summaries, all have quizzes (5-10 questions each)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1) - Core Textbook: Can start after Foundational (Phase 2)
  - User Story 2 (P2) - Summaries: Can start after Foundational (Phase 2) - technically independent but references chapter content
  - User Story 3 (P3) - Quizzes: Can start after Foundational (Phase 2) - technically independent but references chapter content
  - User Story 4 (P4) - Search: Can start after Foundational (Phase 2) - independent, Docusaurus built-in
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Core Textbook**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2) - Summaries**: Can start after Foundational (Phase 2) - Logically depends on chapter content but technically independent (can add summaries before/during chapter authoring)
- **User Story 3 (P3) - Quizzes**: Can start after Foundational (Phase 2) - Logically depends on chapter content but technically independent (can create quizzes before/during chapter authoring)
- **User Story 4 (P4) - Search**: Can start after Foundational (Phase 2) - Completely independent, Docusaurus configuration only

**Recommendation**: Implement in priority order (P1 → P2 → P3 → P4) for incremental value delivery, but P2/P3/P4 can be worked on in parallel if team capacity allows.

### Within Each User Story

**User Story 1 (Core Textbook)**:
- T013 (intro.md) can start immediately after Foundational
- T014-T021 (all 8 chapters) can run in PARALLEL - different files, no dependencies
- T022 (add math equations) depends on chapters existing (T014-T021)
- T023-T024 (images) can run in parallel with chapter authoring
- T025 (build check) depends on all chapters complete
- T026 (Lighthouse) depends on build succeeding
- T027 (deploy) depends on Lighthouse passing

**User Story 2 (Summaries)**:
- T028-T030 (Summary component) can start immediately after Foundational
- T031-T038 (add summaries to chapters) depend on component existing (T028-T030) AND chapters existing (US1 T014-T021)
  - However, T031-T038 can run in PARALLEL - different chapter files
- T039 (mobile verification) depends on all summaries added

**User Story 3 (Quizzes)**:
- T040 (TypeScript types) can start immediately after Foundational
- T041-T047 (Quiz component) can start after types (T040)
- T048-T055 (quiz data for each chapter) can run in PARALLEL - different files
- T056 (add imports) depends on Quiz component (T041-T047) AND quiz data (T048-T055)
- T057-T058 (verification) depend on all quiz tasks complete

**User Story 4 (Search)**:
- T059-T063 all sequential (Docusaurus configuration)
- No parallelization opportunities within this story (only 5 tasks)

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T006, T007, T008 can run in parallel (5 tasks)

**Phase 2 (Foundational)**: T011, T012 can run in parallel (2 tasks)

**Phase 3 (User Story 1)**:
- T013-T021 can run in parallel (9 chapter files)
- T023 (images) can run in parallel with chapter authoring

**Phase 4 (User Story 2)**:
- T031-T038 can run in parallel (8 summary additions)

**Phase 5 (User Story 3)**:
- T048-T055 can run in parallel (8 quiz data creations)

**Phase 7 (Polish)**:
- T064, T065, T066, T067, T069 can run in parallel (5 tasks)

---

## Parallel Example: User Story 1 (Core Textbook)

```bash
# After Foundational phase complete, launch all chapter authoring tasks together:
Task: "Create docs/intro.md with homepage content"
Task: "Create docs/chapter-01-intro-physical-ai.mdx with 1500-3000 words"
Task: "Create docs/chapter-02-sensors-perception.mdx with 1500-3000 words"
Task: "Create docs/chapter-03-kinematics-dynamics.mdx with 1500-3000 words"
Task: "Create docs/chapter-04-motion-planning.mdx with 1500-3000 words"
Task: "Create docs/chapter-05-control-systems.mdx with 1500-3000 words"
Task: "Create docs/chapter-06-learning-adaptation.mdx with 1500-3000 words"
Task: "Create docs/chapter-07-human-robot-interaction.mdx with 1500-3000 words"
Task: "Create docs/chapter-08-real-world-applications.mdx with 1500-3000 words"
Task: "Add diagrams to static/img/ subdirectories"

# After all chapters exist, run:
Task: "Add math equations to chapters using KaTeX syntax"
Task: "Build and verify bundle size <500KB per page"
```

---

## Parallel Example: User Story 2 (Summaries)

```bash
# After Summary component created AND chapters exist, launch all summary additions together:
Task: "Add Summary component to docs/chapter-01-intro-physical-ai.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-02-sensors-perception.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-03-kinematics-dynamics.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-04-motion-planning.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-05-control-systems.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-06-learning-adaptation.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-07-human-robot-interaction.mdx with 3-5 bullets"
Task: "Add Summary component to docs/chapter-08-real-world-applications.mdx with 3-5 bullets"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T012) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 1 (T013-T027) - Core Textbook
4. **STOP and VALIDATE**: Test all 8 chapters independently
   - Manual navigation test (all chapters visible, content renders)
   - Mobile responsiveness test (375px viewport, no horizontal scroll)
   - Performance test (Lighthouse score ≥90, page load <2s)
5. Deploy/demo if ready - **THIS IS A VIABLE MVP**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Core Textbook) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Summaries) → Test independently → Deploy/Demo
4. Add User Story 3 (Quizzes) → Test independently → Deploy/Demo
5. Add User Story 4 (Search) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: User Story 1 (Core Textbook) - T013-T027
   - **Developer B**: User Story 2 (Summaries) - T028-T039 (waits for US1 chapters as needed)
   - **Developer C**: User Story 3 (Quizzes) - T040-T058 (waits for US1 chapters as needed)
   - **Developer D**: User Story 4 (Search) - T059-T063
3. Stories complete and integrate independently

**Note**: In practice, US2/US3 will wait for US1 chapter content, so sequential execution (P1→P2→P3→P4) is most practical for small teams.

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability (US1, US2, US3, US4)
- **Each user story is independently completable and testable** (deploy after each story for incremental value)
- **No test tasks** included because tests were NOT requested in the specification
- **Content authoring** (chapters, summaries, quizzes) is the most time-consuming part (~2-5 days total)
- **Verify checkpoints** after each phase to ensure story independence works
- **Commit after each task** or logical group for easy rollback
- **Stop at any checkpoint** to validate story independently before proceeding

**Avoid**:
- Vague tasks without file paths
- Tasks that modify the same file simultaneously (not [P])
- Cross-story dependencies that break independence (US2/US3/US4 should work even if others incomplete, though content references are logical)
