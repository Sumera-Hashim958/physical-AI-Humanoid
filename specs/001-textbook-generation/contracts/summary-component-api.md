# Contract: Summary Component API

**Component**: `<Summary>`
**Type**: React Component (MDX-compatible)
**Version**: 1.0.0
**Purpose**: Collapsible chapter summary component for quick revision

## Component Interface

### Import

```typescript
import Summary from '@site/src/components/Summary';
```

### Props

```typescript
interface SummaryProps {
  bullets: string[];           // 3-5 key points (required)
  title?: string;              // Summary section title (default: "Chapter Summary")
  collapsible?: boolean;       // Allow collapse/expand (default: false)
  defaultCollapsed?: boolean;  // Initial collapsed state (default: false)
}
```

## Usage Examples

### Basic Usage

```mdx
---
title: "Introduction to Physical AI"
---

# Introduction to Physical AI

[... chapter content ...]

## Chapter Summary

<Summary bullets={[
  "Physical AI combines perception, reasoning, and action in embodied agents",
  "Key challenges include uncertainty, real-time constraints, and safety",
  "Applications span manufacturing, healthcare, and autonomous systems"
]} />
```

### Advanced Usage (Custom Title, Collapsible)

```mdx
<Summary
  title="Key Takeaways"
  bullets={[
    "LIDAR sensors measure distance using laser pulses with millimeter accuracy",
    "Camera-based perception requires computationally expensive computer vision algorithms",
    "Sensor fusion combines multiple modalities for robust environment understanding",
    "Trade-off exists between sensor accuracy and computational cost",
    "Real-time constraints limit the complexity of perception algorithms"
  ]}
  collapsible={true}
  defaultCollapsed={false}
/>
```

## Behavior Specification

### Rendering

1. **Default State** (non-collapsible):
   - Section heading: "Chapter Summary" (or custom `title`)
   - Bulleted list of 3-5 key points
   - Styled box with light background (visually separated from main content)

2. **Collapsible State**:
   - Section heading with chevron icon (▼ expanded, ► collapsed)
   - Click to toggle visibility of bullet points
   - Initial state: expanded (unless `defaultCollapsed = true`)

### Visual Design

```css
/* Default styling (to be implemented in component) */
.summary-container {
  background: var(--ifm-color-secondary-lightest);
  border-left: 4px solid var(--ifm-color-primary);
  padding: 16px 24px;
  margin: 24px 0;
  border-radius: 8px;
}

.summary-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--ifm-color-primary);
}

.summary-list {
  margin: 0;
  padding-left: 24px;
  line-height: 1.8;
}

.summary-list li {
  margin-bottom: 8px;
}
```

### Mobile Responsiveness

- **Touch Targets**: Title/chevron tap area ≥44px height (if collapsible)
- **Font Size**: ≥14px on mobile (SC-005 compliance)
- **Padding**: Adjust padding to 12px on mobile (320px-767px viewports)
- **No Horizontal Scroll**: Bullet text wraps on narrow screens

### Accessibility (WCAG 2.1 AA)

- **Keyboard Navigation**:
  - Tab to summary title (if collapsible)
  - Enter/Space to toggle expand/collapse

- **Screen Reader Support**:
  - ARIA: `role="region"`, `aria-labelledby="summary-heading"`
  - Collapsible: `aria-expanded="true|false"` on toggle button
  - List semantics: `<ul>` with `<li>` elements (not `<div>` styled as bullets)

- **Visual**:
  - High contrast in dark mode (border/background colors adjust)
  - Focus indicator on title (if collapsible)

## Validation Rules

### Input Validation (Build-Time)

1. **Bullet Count** (from FR-005):
   - Minimum: 3 bullets
   - Maximum: 5 bullets
   - **Error if violated**:
     ```
     Error: Summary component requires 3-5 bullets (received {count})
     ```

2. **Bullet Length**:
   - Recommended: 50-200 characters per bullet
   - Maximum: 300 characters per bullet
   - **Warning if exceeded** (build still succeeds):
     ```
     Warning: Summary bullet #{index} is {length} chars (recommended: <200 chars)
     ```

3. **Empty Bullets**:
   - No empty strings allowed
   - **Error if violated**:
     ```
     Error: Summary bullet #{index} cannot be empty
     ```

### TypeScript Interface Enforcement

```typescript
// Compile-time checks
const Summary: React.FC<SummaryProps> = ({ bullets, title, collapsible, defaultCollapsed }) => {
  // Runtime validation (development only)
  if (process.env.NODE_ENV === 'development') {
    if (bullets.length < 3 || bullets.length > 5) {
      throw new Error(`Summary requires 3-5 bullets (received ${bullets.length})`);
    }
    if (bullets.some(b => !b.trim())) {
      throw new Error('Summary bullets cannot be empty');
    }
  }

  // Component logic...
};
```

## Interaction Flow

### Non-Collapsible (Default)

1. User scrolls to summary section
2. Summary is immediately visible (no interaction required)
3. User reads 3-5 bullet points
4. (Optional) User copies bullets for notes

### Collapsible (if `collapsible={true}`)

1. User scrolls to summary section
2. Summary is visible (unless `defaultCollapsed={true}`)
3. User clicks title/chevron to toggle:
   - **Collapsed**: Hide bullets, chevron points right (►)
   - **Expanded**: Show bullets, chevron points down (▼)
4. State persists during session (optional: save to localStorage)

## Performance

- **Rendering**: Component mounts in <50ms
- **Interaction** (if collapsible): Toggle animation completes in <200ms
- **Bundle Size**: Summary component <5KB (gzipped)

## Testing Contract

### Unit Tests

1. **Rendering**:
   - ✅ Component renders with 3-5 bullets
   - ✅ Custom title renders correctly
   - ✅ Default title "Chapter Summary" used if none provided

2. **Validation**:
   - ✅ Error thrown if bullets.length < 3 or > 5
   - ✅ Error thrown if bullets contain empty strings

3. **Collapsible Behavior**:
   - ✅ Chevron icon changes on toggle
   - ✅ Bullets hidden when collapsed
   - ✅ Initial state matches `defaultCollapsed` prop

### Integration Tests

1. **MDX Integration**:
   - ✅ Component renders in chapter MDX
   - ✅ Styling consistent with Docusaurus theme

2. **Accessibility**:
   - ✅ Keyboard navigation works (Tab, Enter/Space)
   - ✅ Screen reader announces summary region

### Manual Tests

1. **Mobile Responsiveness**:
   - ✅ Readable on iPhone SE (375px width)
   - ✅ Touch target ≥44px (if collapsible)
   - ✅ No horizontal scrolling

2. **Visual Design**:
   - ✅ Summary visually distinct from main content
   - ✅ Bullet points aligned and readable
   - ✅ Works in light and dark mode

## Example Outputs

### Rendered HTML (Non-Collapsible)

```html
<div class="summary-container" role="region" aria-labelledby="summary-heading">
  <h2 id="summary-heading" class="summary-title">Chapter Summary</h2>
  <ul class="summary-list">
    <li>Physical AI combines perception, reasoning, and action in embodied agents</li>
    <li>Key challenges include uncertainty, real-time constraints, and safety</li>
    <li>Applications span manufacturing, healthcare, and autonomous systems</li>
  </ul>
</div>
```

### Rendered HTML (Collapsible, Expanded)

```html
<div class="summary-container" role="region" aria-labelledby="summary-heading">
  <button
    class="summary-toggle"
    aria-expanded="true"
    aria-controls="summary-content"
    id="summary-heading"
  >
    <span class="summary-title">Chapter Summary</span>
    <span class="chevron">▼</span>
  </button>
  <div id="summary-content" class="summary-content">
    <ul class="summary-list">
      <li>Physical AI combines perception, reasoning, and action in embodied agents</li>
      <li>Key challenges include uncertainty, real-time constraints, and safety</li>
      <li>Applications span manufacturing, healthcare, and autonomous systems</li>
    </ul>
  </div>
</div>
```

## Constraints

1. **Bullet Count** (from FR-005):
   - Minimum: 3 bullets
   - Maximum: 5 bullets

2. **Text Length Recommendations**:
   - Per bullet: 50-200 characters (recommended)
   - Per bullet: 300 characters (maximum)
   - Total summary: <500 words (for mobile readability)

3. **Performance Budget**:
   - Component load time: <50ms
   - Toggle animation: <200ms (if collapsible)
   - Bundle size: <5KB (gzipped)

## Dependencies

- **React**: ^18.0.0 (for component logic)
- **Docusaurus Theme**: Custom CSS variables (colors, spacing)
- **No External Libraries**: Pure React, no animation libraries (keeps bundle small)

## Future Enhancements (Out of Scope for P1-P3)

- ⏭️ Print-friendly styling (summary on separate page when printing)
- ⏭️ Copy-to-clipboard button (one-click copy all bullets)
- ⏭️ Summary highlights in main content (link bullets to chapter sections)
- ⏭️ AI-generated summaries (integration with 002-rag-chatbot)

## Version History

- **1.0.0** (2025-12-17): Initial contract for P1-P3 features
