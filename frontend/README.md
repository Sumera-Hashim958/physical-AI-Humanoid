# Physical AI Textbook - Frontend

Docusaurus-based interactive textbook with embedded AI chatbot.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm start
```

The site will open at http://localhost:3000

### 3. Build for Production

```bash
npm run build
```

### 4. Serve Production Build

```bash
npm run serve
```

## Project Structure

```
frontend/
├── docs/                  # Textbook chapters (MDX files)
│   ├── intro.md          # Homepage/Introduction
│   ├── chapter-01-intro-physical-ai.mdx
│   ├── chapter-02-sensors-perception.mdx
│   └── ...
├── src/                   # React components
│   ├── pages/            # Custom pages
│   │   ├── index.js      # Landing page
│   │   └── index.module.css
│   └── css/              # Global styles
│       └── custom.css
├── static/                # Static assets
│   └── img/              # Images
├── docusaurus.config.js   # Docusaurus configuration
├── sidebars.js           # Sidebar navigation
├── package.json          # Dependencies
└── tsconfig.json         # TypeScript config
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run serve` - Serve production build locally
- `npm run clear` - Clear Docusaurus cache
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run typecheck` - Run TypeScript type checking

## Features

- 📚 **7 Chapters** on Physical AI & Humanoid Robotics
- 🤖 **AI Chatbot** (to be integrated) - Ask questions about content
- 📱 **Mobile-First Design** - Responsive on all devices
- 🎨 **Modern UI** - Clean, fast, accessible
- 📖 **Math Support** - KaTeX for equations
- 🔍 **Search** - Full-text search across all content

## Adding Content

### Add a New Chapter

1. Create a new MDX file in `docs/`:
   ```mdx
   ---
   id: chapter-08-new-topic
   title: Chapter 8 - New Topic
   sidebar_position: 8
   ---

   # Chapter 8: New Topic

   Your content here...
   ```

2. Add to `sidebars.js`:
   ```js
   {
     type: 'category',
     label: 'Chapters',
     items: [
       // ...existing chapters
       'chapter-08-new-topic',
     ],
   },
   ```

### Add Interactive Elements

Use MDX to embed React components:

```mdx
import Quiz from '@site/src/components/Quiz';

<Quiz questions={[...]} />
```

## Integration with Backend

The chat widget will connect to the FastAPI backend at:
- Development: http://localhost:8000
- Production: (to be configured)

See `../backend/README.md` for backend setup.

## Deployment

Deploy to Vercel or Netlify:

```bash
npm run build
# Upload `build/` folder to hosting platform
```

Or use automatic deployment via GitHub integration.

## Development Guidelines

See `../.specify/memory/constitution.md` for full guidelines.

**Key Principles**:
- Mobile-first responsive design
- Page load <2 seconds
- Keep bundle size minimal
- No heavy dependencies

## Troubleshooting

### Port 3000 already in use

```bash
npx kill-port 3000
```

### Build fails

```bash
npm run clear
npm install
npm run build
```

### TypeScript errors

```bash
npm run typecheck
```
