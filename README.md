# Physical AI & Humanoid Robotics Interactive Textbook

An AI-native interactive textbook with embedded RAG chatbot, personalization, and Urdu translation support.

## Project Structure

```
/BOOK (root)
├── frontend/              # Docusaurus textbook
│   ├── docs/             # Chapter content (MDX)
│   ├── src/              # React components
│   └── package.json
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   └── models/       # Data schemas
│   ├── main.py           # Entry point
│   └── requirements.txt
├── .specify/             # SpecKit Plus templates
├── specs/                # Feature specifications
├── history/              # Prompt history & ADRs
└── .claude/              # Claude Code configuration
```

## Quick Start

### Frontend (Docusaurus)

```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs at http://localhost:8000/docs

## Features

### Current (v1.0)
- ✅ 7 chapters on Physical AI & Humanoid Robotics
- ✅ Modern responsive design
- ✅ Math equations support (KaTeX)
- ✅ Full-text search
- ✅ Mobile-optimized

### Planned (v1.1)
- 🚧 RAG Chatbot (Claude API)
- 🚧 Personalization (beginner/intermediate/advanced)
- 🚧 Urdu translation
- 🚧 Progress tracking
- 🚧 User authentication

## Technology Stack

### Frontend
- **Framework**: Docusaurus 3.x
- **Language**: TypeScript, React
- **Styling**: CSS Modules
- **Deployment**: Vercel / Netlify

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Postgres (free tier)
- **Vector DB**: Qdrant Cloud (free tier)
- **AI**: Claude API (Anthropic)
- **Deployment**: Railway

## Development Workflow

This project uses **Spec-Driven Development**:

1. **Specify**: Document feature in `specs/<feature>/spec.md`
2. **Plan**: Architecture in `specs/<feature>/plan.md`
3. **Tasks**: Break down in `specs/<feature>/tasks.md`
4. **Implement**: Code with references to tasks
5. **Test**: Verify each module
6. **Deploy**: Merge to main → auto-deploy

See `.specify/memory/constitution.md` for full guidelines.

## Core Principles

1. **AI-Native First** - Claude API for all intelligence (RAG, personalization, translation)
2. **Performance** - <2s page load, <3s chat response
3. **Simplicity** - Clean, minimal architecture
4. **Modular** - Frontend/backend separation
5. **Cost-Conscious** - <$10/day for 100 users
6. **Mobile-First** - Responsive design

## Documentation

- **Constitution**: `.specify/memory/constitution.md`
- **Frontend Guide**: `frontend/README.md`
- **Backend Guide**: `backend/README.md`
- **Feature Specs**: `specs/`
- **ADRs**: `history/adr/`

## Contributing

1. Create a feature branch: `git checkout -b 00X-feature-name`
2. Write specification in `specs/00X-feature-name/`
3. Implement following constitution guidelines
4. Test locally (frontend + backend)
5. Create PR with spec/task references

## License

[Add your license here]

## Support

For issues or questions, see:
- Frontend issues: `frontend/README.md#troubleshooting`
- Backend issues: `backend/README.md#troubleshooting`
- Constitution: `.specify/memory/constitution.md`
