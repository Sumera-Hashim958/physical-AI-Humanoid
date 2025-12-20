# Implementation Plan: Textbook Content Generation

**Branch**: `001-textbook-generation` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-textbook-generation/spec.md`

## Summary

Build a static educational textbook with 6-8 chapters on Physical AI and Humanoid Robotics using Docusaurus. Each chapter includes core content (1500-3000 words), a 3-5 point summary, and 5-10 quiz questions with explanations. Content is stored as Markdown files, rendered as static HTML, and optimized for mobile-first, fast-loading experience (<2s page loads on 3G). No backend required for P1-P3; all functionality is client-side static content.

**Technical Approach**: Use Docusaurus for static site generation with MDX for interactive quiz components. Chapter content written in Markdown, quizzes implemented as React components embedded via MDX, search provided by Docusaurus built-in plugin. Deploy to Vercel for instant builds and edge caching.

## Technical Context

**Language/Version**: JavaScript/TypeScript (Node.js 18+), React 18+
**Primary Dependencies**: Docusaurus 3.x, MDX (for interactive quiz components), KaTeX (for math equations), Prism (syntax highlighting)
**Storage**: Static Markdown files in `/docs` directory (Docusaurus convention); no database required for static content
**Testing**: Manual testing for content rendering, Lighthouse CI for performance validation (<2s loads, <500KB bundles)
**Target Platform**: Web (static site), deployed to Vercel; optimized for mobile browsers (iOS Safari, Chrome Android)
**Project Type**: Web (static site only - no backend for P1-P3)
**Performance Goals**: <2s page load on 3G, <500ms quiz interactions, <60s build time, <500KB bundle size (gzipped)
**Constraints**: Mobile-first (<14px readable fonts, no horizontal scroll), free-tier deployment (Vercel), no backend APIs for static content
**Scale/Scope**: 6-8 chapters (~12,000-24,000 words total), 40-80 quiz questions, 24-40 summary bullets, <10 concurrent authors

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: AI-Native First
- ⚠️ **DEFERRED**: This feature (textbook-generation) provides static content. AI-native capabilities (RAG chatbot, AI-generated summaries/quizzes) are covered in future features (002-rag-chatbot, etc.)
- **Current Feature**: Static Markdown content (manually authored or AI-assisted authoring, then reviewed)
- **Compliance**: PASS (with future dependency) - This feature creates the content foundation that RAG will consume

### Principle II: Performance & Speed (NON-NEGOTIABLE)
- ✅ **PASS**: <2s page loads on 3G (SC-002), <500ms quiz interactions (SC-007), <500KB bundle (SC-009)
- **Implementation**: Static site generation, edge caching, code splitting, optimized images

### Principle III: Simplicity & Minimalism
- ✅ **PASS**: Docusaurus is a well-established, minimal static site generator; no custom build pipeline needed
- **Implementation**: Use Docusaurus defaults, MDX for quizzes (built-in), KaTeX plugin (official)

### Principle IV: Modular Architecture
- ✅ **PASS**: Textbook content is independent module; can be consumed by RAG chatbot, translation service, etc.
- **Implementation**: Clean separation between content (Markdown), presentation (Docusaurus), and future features (RAG backend)

### Principle V: Free-Tier & Cost Constraints
- ✅ **PASS**: Vercel free tier (100GB bandwidth/month, unlimited builds for hobby projects)
- **Implementation**: Static site hosting, no compute costs, CDN included

### Principle VI: Rapid Deployment
- ✅ **PASS**: Docusaurus builds in <60s, Vercel deploys in <30s (total <90s from push to live)
- **Implementation**: GitHub Actions → Vercel auto-deploy on push to main

### Principle VII: Grounded & Accurate Responses
- ⚠️ **DEFERRED**: Applies to RAG chatbot (002-rag-chatbot), not static textbook content
- **Current Feature**: Content accuracy ensured by manual review process
- **Compliance**: N/A for this feature

### Principle VIII: Mobile-First Design
- ✅ **PASS**: Docusaurus is mobile-responsive by default; SC-005 ensures ≥14px fonts, no horizontal scroll
- **Implementation**: Responsive Docusaurus theme, touch-friendly navigation, optimized for mobile viewports

**Gate Status**: ✅ **PASS** - All applicable principles satisfied; Principles I and VII intentionally deferred to future features

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── quiz-component-api.md  # MDX component interface for quizzes
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docs/                    # Docusaurus content directory
├── intro.md             # Homepage/landing page
├── chapter-01-intro-physical-ai.md
├── chapter-02-sensors-perception.md
├── chapter-03-kinematics-dynamics.md
├── chapter-04-motion-planning.md
├── chapter-05-control-systems.md
├── chapter-06-learning-adaptation.md
├── chapter-07-human-robot-interaction.md
├── chapter-08-real-world-applications.md
└── _components/         # MDX components for interactive elements
    ├── Quiz.tsx         # Quiz component (question display, answer validation)
    ├── Summary.tsx      # Summary component (collapsible, styled)
    └── ChapterNav.tsx   # Previous/next chapter navigation

src/                     # Docusaurus custom code
├── components/          # React components
│   └── QuizEngine/      # Quiz logic (state management, scoring, feedback)
├── css/                 # Custom styles
│   └── custom.css       # Mobile-first overrides, brand colors
└── pages/               # Custom pages (optional)

static/                  # Static assets
├── img/                 # Chapter diagrams, illustrations
│   ├── sensors/
│   ├── kinematics/
│   └── ...
└── katex/               # KaTeX fonts (for math equations)

docusaurus.config.js     # Docusaurus configuration
package.json             # Dependencies (Docusaurus, React, KaTeX, etc.)
tsconfig.json            # TypeScript config
.github/                 # CI/CD
└── workflows/
    └── deploy.yml       # Vercel auto-deploy
```

**Structure Decision**: Static site (Option 1 variant) - No backend needed for P1-P3. Docusaurus manages build, routing, and navigation. All content is Markdown in `/docs`, custom components in `/src/components`. This aligns with Principle III (Simplicity) and enables <60s builds (Principle VI).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - table not needed.

---

## Post-Design Constitution Re-Check

**Re-evaluated**: 2025-12-17 (after Phase 1 design complete)

### Updated Assessments

All principles remain **PASS** after detailed design:

1. **Principle II (Performance)**: ✅ CONFIRMED
   - Research shows KaTeX is 5-10x faster than MathJax
   - Code splitting ensures <500KB bundles per page
   - Vercel edge caching provides <200ms TTFB

2. **Principle III (Simplicity)**: ✅ CONFIRMED
   - Quiz component: <30KB, pure React (no external libs)
   - Summary component: <5KB, minimal styling
   - No custom build pipeline needed (Docusaurus handles all)

3. **Principle IV (Modular Architecture)**: ✅ CONFIRMED
   - Markdown files are canonical source (easily consumed by future RAG pipeline)
   - Components reusable across chapters
   - Static content decoupled from future backend features

4. **Principle VI (Rapid Deployment)**: ✅ CONFIRMED
   - Docusaurus build: ~30-45s for 8 chapters (measured in research)
   - Vercel deploy: ~20-30s
   - Total: <90s ✅

**No new violations introduced during design phase.**

**Gate Status**: ✅ **FINAL PASS** - Ready for `/sp.tasks`

---

## Design Artifacts Summary

| Artifact | Status | Location | Key Decisions |
|----------|--------|----------|---------------|
| **Research** | ✅ Complete | `research.md` | Docusaurus 3.x, MDX, KaTeX, Vercel |
| **Data Model** | ✅ Complete | `data-model.md` | File-based storage, 4 entities, ~1.5-5MB total |
| **API Contracts** | ✅ Complete | `contracts/quiz-component-api.md`, `contracts/summary-component-api.md` | React components, TypeScript interfaces, validation rules |
| **Quickstart** | ✅ Complete | `quickstart.md` | 15min setup, 2-5 days content authoring |

**Next Step**: Run `/sp.tasks` to generate implementation task list

**Estimated Implementation Time**: 3-5 days (1 day setup + components, 2-4 days content authoring)
