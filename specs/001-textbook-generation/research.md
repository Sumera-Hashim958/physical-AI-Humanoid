# Research: Textbook Content Generation

**Feature**: 001-textbook-generation
**Date**: 2025-12-17
**Status**: Complete

## Research Questions

1. **Docusaurus Best Practices** - How to structure educational content for optimal performance and UX?
2. **MDX for Interactive Content** - Best patterns for embedding React components (quizzes) in Markdown?
3. **Math Rendering** - KaTeX vs MathJax for Physical AI equations?
4. **Performance Optimization** - How to achieve <2s page loads and <500KB bundles?
5. **Mobile-First Design** - Docusaurus theme customization for touch-friendly navigation?

---

## 1. Docusaurus Best Practices for Educational Content

### Decision: Use Docusaurus 3.x with Sidebar Navigation

**Rationale**:
- Docusaurus is purpose-built for documentation/educational content
- Built-in sidebar navigation enables <2-click chapter navigation (SC-006)
- Automatic table of contents generation (FR-014)
- Built-in search plugin (P4 requirement)
- Static site generation ensures <2s page loads (SC-002)

**Implementation Patterns**:
- **Sidebar Configuration**: Define all 6-8 chapters in `sidebars.js` with clear category structure
- **Chapter Structure**: Each chapter is a separate `.md` or `.mdx` file in `/docs`
- **Frontmatter Metadata**: Use YAML frontmatter for chapter number, title, description, last updated date
- **Navigation**: Enable previous/next links at bottom of each chapter (built-in Docusaurus feature)

**Alternatives Considered**:
- **Gatsby**: More flexible but heavier build times (>60s for small sites), violates Principle VI
- **Next.js SSG**: Requires more custom configuration, less optimized for educational content
- **VuePress**: Smaller ecosystem, fewer plugins for math/search

**Best Practices from Docusaurus Docs**:
- Keep each chapter file under 5000 words for fast parsing
- Use lazy-loaded images with `<img loading="lazy">`
- Enable code splitting in `docusaurus.config.js`
- Use `@docusaurus/preset-classic` for sensible defaults

---

## 2. MDX for Interactive Quizzes

### Decision: Use MDX with Custom React Quiz Component

**Rationale**:
- MDX allows embedding React components directly in Markdown (FR-006, FR-015)
- Enables client-side interactivity without backend (Principle III: Simplicity)
- Quiz state managed in browser (localStorage for retake prevention)
- Immediate feedback without server round-trip (<500ms, SC-007)

**Implementation Pattern**:

```mdx
<!-- chapter-01-intro-physical-ai.mdx -->

## Chapter Summary

<Summary bullets={[
  "Physical AI combines robotics, perception, and intelligent control",
  "Embodied intelligence requires real-time sensor processing",
  "Key challenges: uncertainty, dynamics, safety"
]} />

## Quiz

<Quiz questions={[
  {
    id: "q1",
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
  // ... more questions
]} />
```

**Component API** (see `contracts/quiz-component-api.md`):
- `<Quiz questions={QuizQuestion[]}>` - Main quiz component
- `<Summary bullets={string[]}>` - Chapter summary component
- Props: `questions`, `showExplanations`, `allowRetake`, `randomize`

**Alternatives Considered**:
- **Pure Markdown with External Quiz Tool**: Requires iframe embeds, slower, breaks offline caching
- **Vanilla JS in Markdown**: Less maintainable, no type safety, harder to test
- **Server-Side Quizzes**: Violates Principle III (complexity), adds backend dependency

**Best Practices**:
- Store quiz data in JSON files imported into MDX (easier authoring than inline JSX)
- Use React hooks for quiz state (useState, useEffect)
- Persist user progress to localStorage (optional for P3)
- Randomize question order on each load (FR-007, acceptance scenario 4)

---

## 3. Math Rendering: KaTeX vs MathJax

### Decision: Use KaTeX via `remark-math` and `rehype-katex`

**Rationale**:
- **Performance**: KaTeX is 5-10x faster than MathJax (important for mobile, Principle II)
- **Bundle Size**: KaTeX fonts ~200KB vs MathJax ~1MB (helps meet SC-009 <500KB target)
- **Docusaurus Integration**: Official plugin support (`@docusaurus/remark-math`)
- **Offline Support**: KaTeX works offline, MathJax requires CDN

**Implementation**:
```bash
npm install remark-math rehype-katex
```

```js
// docusaurus.config.js
presets: [
  [
    'classic',
    {
      docs: {
        remarkPlugins: [require('remark-math')],
        rehypePlugins: [require('rehype-katex')],
      },
    },
  ],
],
stylesheets: [
  {
    href: 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
    type: 'text/css',
    integrity: 'sha384-...',
    crossorigin: 'anonymous',
  },
],
```

**Usage in Chapters**:
```markdown
Inline math: The position vector $\vec{p} = [x, y, z]^T$

Block equation:

$$
\tau = J(\theta)^T F_{ext}
$$
```

**Alternatives Considered**:
- **MathJax**: Better font quality, slower rendering, larger bundle
- **Images for Equations**: Not searchable, accessibility issues, manual effort

**Physical AI Equation Examples** (from FR-012):
- Kinematics: $v = \frac{d}{dt}p(t)$, $a = \frac{d}{dt}v(t)$
- Dynamics: $\tau = I\alpha$ (torque = moment of inertia × angular acceleration)
- Control: $u(t) = K_p e(t) + K_i \int e(t) dt + K_d \frac{d}{dt}e(t)$ (PID control)

---

## 4. Performance Optimization Strategies

### Decision: Multi-Layered Optimization Approach

**Target Metrics** (from Success Criteria):
- SC-002: <2s page load on 3G connection
- SC-007: <500ms quiz interactions
- SC-009: <500KB bundle size (gzipped)

**Optimization Techniques**:

#### 4.1 Build-Time Optimizations
- **Code Splitting**: Docusaurus automatically splits by route; each chapter is separate bundle
- **Tree Shaking**: Remove unused React components, KaTeX glyphs
- **Minification**: Terser for JS, cssnano for CSS (built into Docusaurus)
- **Image Optimization**: Use WebP format, lazy loading, responsive images

```js
// docusaurus.config.js
module.exports = {
  webpack: {
    jsLoader: (isServer) => ({
      loader: require.resolve('esbuild-loader'), // 10x faster than Babel
      options: {
        target: 'es2017',
      },
    }),
  },
};
```

#### 4.2 Runtime Optimizations
- **Lazy Load Quizzes**: Use `React.lazy()` to defer quiz component until user scrolls to bottom
- **Memoization**: `React.memo()` for quiz questions to prevent re-renders
- **Virtual Scrolling**: For long chapters (>3000 words), implement intersection observer for "Back to Top" button

#### 4.3 Network Optimizations
- **Vercel Edge Caching**: Static assets served from CDN closest to user
- **HTTP/2 Push**: Preload critical CSS/fonts
- **Compression**: Brotli compression (better than gzip for text, ~20% smaller)

#### 4.4 Mobile-Specific
- **Touch Event Optimization**: Use `passive` event listeners for scroll
- **Reduced Animations**: Respect `prefers-reduced-motion` for low-end devices
- **Font Subsetting**: Load only Latin + Math glyphs (exclude Cyrillic, CJK for initial release)

**Monitoring**:
- Lighthouse CI in GitHub Actions (fail build if score <90)
- Bundle size tracking with `@next/bundle-analyzer` equivalent

**Baseline Target**:
- Initial page load (Chapter 1): ~300KB HTML+JS+CSS (gzipped)
- Subsequent chapters: ~50KB each (shared bundles cached)
- Quiz component: ~30KB (lazy loaded)

---

## 5. Mobile-First Docusaurus Theme Customization

### Decision: Customize Docusaurus Classic Theme with Mobile Overrides

**Requirements** (from SC-005):
- Font size ≥14px on mobile
- No horizontal scrolling
- Touch-friendly navigation (≥44px tap targets per iOS HIG)

**Implementation**:

#### 5.1 Typography
```css
/* src/css/custom.css */
:root {
  --ifm-font-size-base: 16px; /* Base font (desktop) */
  --ifm-line-height-base: 1.6; /* Readable line spacing */
}

@media (max-width: 768px) {
  :root {
    --ifm-font-size-base: 14px; /* SC-005 requirement */
    --ifm-heading-font-size-multiplier: 1.2; /* Larger headings on mobile */
  }

  /* Prevent code blocks from horizontal scroll */
  pre {
    overflow-x: auto;
    max-width: 100vw;
  }

  /* Responsive tables */
  table {
    display: block;
    overflow-x: auto;
  }
}
```

#### 5.2 Touch-Friendly Navigation
```css
/* Sidebar links - 44px tap targets */
.menu__link {
  min-height: 44px;
  padding: 12px 16px;
}

/* Previous/Next buttons */
.pagination-nav__link {
  min-height: 56px; /* Larger for thumbs */
  font-size: 18px;
}

/* Quiz answer buttons */
.quiz-option {
  min-height: 48px;
  padding: 12px 20px;
  margin: 8px 0;
  border-radius: 8px;
  touch-action: manipulation; /* Disable double-tap zoom */
}
```

#### 5.3 Responsive Images
```markdown
<!-- In chapters, use Docusaurus image component -->
![Sensor array diagram](./img/sensor-array.png)
```

```css
/* Ensure images don't overflow on mobile */
img {
  max-width: 100%;
  height: auto;
}
```

#### 5.4 Sticky Navigation
```js
// docusaurus.config.js
themeConfig: {
  navbar: {
    hideOnScroll: false, // Keep navbar visible for easy chapter switching
  },
  docs: {
    sidebar: {
      hideable: true, // Collapsible sidebar on mobile
      autoCollapseCategories: true,
    },
  },
}
```

**Testing Strategy**:
- Manual testing on iOS Safari (iPhone SE - smallest modern viewport)
- Chrome DevTools mobile emulation (3G throttling)
- Lighthouse mobile audit (target: 90+ performance score)

**Accessibility**:
- ARIA labels for quiz buttons
- Keyboard navigation for all interactive elements
- Focus indicators (2px outline) for tab navigation

---

## Summary of Decisions

| Aspect | Decision | Key Rationale |
|--------|----------|---------------|
| **Framework** | Docusaurus 3.x | Purpose-built for docs, <60s builds, built-in search |
| **Interactive Content** | MDX + React components | Client-side interactivity, no backend needed |
| **Math Rendering** | KaTeX | 5-10x faster than MathJax, <200KB bundle |
| **Performance** | Code splitting + edge caching + lazy loading | Meets <2s loads, <500KB bundles |
| **Mobile Design** | Custom CSS overrides + responsive components | ≥14px fonts, 44px tap targets, no horizontal scroll |
| **Deployment** | Vercel | Free tier, <30s deploys, edge CDN |

**No Unresolved Clarifications** - All technical decisions made based on constitution constraints and success criteria.

**Next Phase**: Phase 1 - Generate data-model.md, contracts/, and quickstart.md.
