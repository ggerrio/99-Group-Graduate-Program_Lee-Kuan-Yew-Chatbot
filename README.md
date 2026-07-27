# Lee Kuan Yew AI Chatbot

An AI-powered chatbot application trained on Lee Kuan Yew's memoirs, speeches, interviews, and articles. The application provides factually grounded, insightful text responses using Retrieval-Augmented Generation (RAG) and Google Gemini 2.5.

---

## 🚀 Project Overview

The **Lee Kuan Yew AI Chatbot** enables users to explore Lee Kuan Yew's perspectives on leadership, governance, economics, geopolitics, and life philosophy. 

This repository contains **Phase 0: Project Foundation & Engineering Setup**, establishing a clean, modular, and production-ready foundation for future development phases.

---

## 🛠 Tech Stack

### Frontend
- **Framework**: React 19 + Vite
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS, CSS Variables Design Tokens
- **UI Components**: shadcn/ui foundation
- **Icons**: Lucide React
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **HTTP Client**: Axios
- **Routing**: React Router v6 (Lazy loaded routes)
- **Formatting**: React Markdown

### Backend
- **Framework**: Python 3.11+ / FastAPI
- **Web Server**: Uvicorn
- **Database**: SQLite (SQLAlchemy 2.0 ORM)
- **Migrations**: Alembic
- **Validation & Settings**: Pydantic v2 / Pydantic Settings
- **Environment Management**: python-dotenv

### AI & Vector Stack (Future Phases)
- **LLM**: Google Gemini 2.5 Flash API
- **RAG Orchestration**: LlamaIndex
- **Vector Database**: Qdrant
- **Embeddings**: BAAI/bge-small-en-v1.5
- **PDF Parser**: PyPDF
- **Evaluation**: Ragas

### Deployment & Containerization
- **Frontend**: Vercel ready
- **Backend**: Docker container-ready (`Dockerfile`)

---

## 🏗 Architecture & Folder Structure

The project strictly adheres to **Clean Architecture** and **Separation of Concerns**.

```
.
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore configuration
├── Dockerfile                # Backend containerization Dockerfile
├── README.md                 # Project documentation
├── alembic.ini               # Alembic database migrations config
├── alembic/                  # Database migration scripts
├── components.json           # shadcn/ui configuration
├── package.json              # Frontend dependencies and scripts
├── requirements.txt          # Python backend dependencies
├── tailwind.config.js        # Tailwind CSS theme configuration
├── tsconfig.json             # TypeScript root configuration
├── vite.config.ts            # Vite bundler & path alias configuration
│
├── app/                      # Python FastAPI Backend Architecture
│   ├── main.py               # FastAPI application entrypoint & lifespan
│   ├── api/                  # API routing and versioned endpoints
│   │   └── v1/
│   │       ├── router.py     # Aggregated v1 API Router
│   │       └── endpoints/    # Feature endpoints (e.g. health check)
│   ├── core/                 # Settings management & logging utilities
│   ├── config/               # Additional module configuration
│   ├── database/             # SQLAlchemy engine, session & base models
│   ├── models/               # ORM database entities (future phases)
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Core business logic services
│   ├── rag/                  # Retrieval-Augmented Generation module
│   ├── ingestion/            # PDF document parsing & chunking
│   ├── prompts/              # System prompts & persona guidelines
│   ├── evaluation/           # Ragas evaluation framework
│   ├── utils/                # General backend utility functions
│   ├── scripts/              # Command-line & operational tools
│   └── tests/                # Automated pytest test suites
│
├── knowledge/                # Raw Corpus Source Documents
│   ├── memoirs/              # LKY Memoirs
│   ├── speeches/             # Public Speeches & Addresses
│   ├── interviews/           # Transcribed Interviews
│   └── articles/             # Articles & Commentary
│
└── src/                      # React Frontend Architecture
    ├── main.tsx              # React entry point
    ├── App.tsx               # App router, providers & layout wrapper
    ├── index.css             # Tailwind base styles & CSS design tokens
    ├── components/           # UI components (shadcn/ui & custom)
    │   ├── ui/               # Reusable primitives (Button, Card, Input)
    │   └── common/           # Shared components (ThemeToggle)
    ├── features/             # Domain-specific feature modules
    ├── hooks/                # Custom React hooks (useTheme)
    ├── layouts/              # MainLayout application shell
    ├── pages/                # Page views (ChatPage, NotFoundPage)
    ├── services/             # Axios API client & endpoints
    ├── store/                # Zustand global state (theme, sidebar)
    ├── types/                # TypeScript interface definitions
    └── lib/                  # Utilities (cn helper)
```

---

## ⚡ Installation & Setup

### Prerequisites
- **Node.js**: v18.0+ or v20.0+
- **Python**: v3.11+
- **Git**

### 1. Clone Repository
```bash
git clone <repository-url>
cd 99-Group-Graduate-Program_Lee-Kuan-Yew-Chatbot
```

### 2. Frontend Setup
```bash
# Install NPM dependencies
npm install

# Start Vite Development Server
npm run dev
```
The frontend application will be running at `http://localhost:3000` (or `http://localhost:5173`).

### 3. Backend Setup
```bash
# Create Python Virtual Environment
python -m venv .venv

# Activate Virtual Environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI Uvicorn Server
uvicorn app.main:app --reload
```
The backend server will be running at `http://localhost:8000`.

---

## 🧪 Development Workflow & Verification

### Health Endpoint Check
Verify backend service status by opening in browser or running:
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "ok"
}
```

### Interactive API Documentation (Swagger)
Access Swagger UI at:
`http://localhost:8000/docs`

### Code Quality & Linting
```bash
# Frontend Typecheck & Lint
npm run typecheck
npm run lint

# Backend Pytest Suite
pytest app/tests
```

---

## 🗺 Future Roadmap

- **Phase 1: Knowledge Ingestion Pipeline** — PDF extraction, text chunking, and metadata parsing from `/knowledge`.
- **Phase 2: Vector Search & Embeddings** — Qdrant vector database integration with `BAAI/bge-small-en-v1.5`.
- **Phase 3: Gemini 2.5 RAG Pipeline** — LlamaIndex RAG chain, system prompt persona, and context-grounded response generation.
- **Phase 4: Interactive Chat UI** — Real-time chat streaming interface, message history, citations, and source viewer.
- **Phase 5: Evaluation & Optimization** — Ragas evaluation benchmarks, latency optimization, and production deployment on Vercel & Docker.
