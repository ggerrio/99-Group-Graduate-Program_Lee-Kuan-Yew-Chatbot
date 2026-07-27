# Lee Kuan Yew AI Chatbot

An AI-powered conversational application designed for the **"What Would Lee Kuan Yew Do?"** challenge. The system preserves the governance philosophy, economic strategies, and foreign policy perspectives of Singapore's founding Prime Minister, **Lee Kuan Yew**, delivering factually grounded answers in his persona backed by direct source citations.

The chatbot is powered by a custom Retrieval-Augmented Generation (RAG) pipeline combining a local vectorized NumPy search index over 5,772 document chunks with Google Gemini API, wrapped in a React frontend and FastAPI backend.

---

## 🏗 System Architecture & End-to-End Flow

The application processes user queries through a multi-stage RAG pipeline:

```
[User Query]
     │
     ▼
[1. Query Normalizer] ──► Collapses punctuation & cleans noise
     │
     ▼
[2. Vector Embedder] ──► BAAI/bge-small-en-v1.5 (384-dim vector)
     │
     ▼
[3. Local Vector Search] ──► Matrix dot-product over 5,772 pre-computed chunks (< 2ms)
     │
     ▼
[4. Context Assembly] ──► Token budget allocation (max 3,000 tokens)
     │
     ▼
[5. Persona Prompting] ──► System prompt with strict anti-fabrication grounding rules
     │
     ▼
[6. Gemini Generation] ──► Generates first-person response or canonical refusal
     │
     ▼
[7. Citation Validator] ──► Verifies document title, year, and page references
     │
     ▼
[Client Response] ──► Text, citation pills, refusal status, post-2015 inference flag
```

---

## 🛠 Tech Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Frontend** | React 19, Vite, TypeScript, Tailwind CSS, shadcn/ui, Zustand, TanStack Query, Lucide React, Framer Motion |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2, Loguru, SQLAlchemy |
| **RAG & Vector Search** | `BAAI/bge-small-en-v1.5` (SentenceTransformers), NumPy vectorized dot-product matrix, Google Gemini API (`gemini-3.5-flash-lite`) |
| **Evaluation Framework** | Custom eval harness (`app/evaluation/`), 60-query gold dataset (`queries.jsonl`), Faithfulness & Persona rubrics |
| **Deployment** | Vercel (Frontend), Railway Docker Container (Backend) |

---

## 💡 Key Architectural Design Decisions

1. **Local NumPy Matrix Retrieval vs. Managed Vector Database**:
   - Rather than introducing an external managed vector DB dependency (such as Qdrant Cloud), the retrieval engine loads 5,772 pre-computed document vector payloads into a pre-normalized $(5772, 384)$ NumPy matrix.
   - Vector similarity is computed via matrix-vector dot product in **$< 1.5\text{ms}$** per query. This minimizes deployment complexity, eliminates network latency to an external database, and ensures $100\%$ reproducible offline search.

2. **Grounding-First Persona Design**:
   - The persona system prompt (`persona_prompt.txt`) prioritizes strict factual grounding over stylistic flourish.
   - **Refusal Mechanism**: If top retrieval similarity falls below threshold ($< 0.35$), the system returns a canonical refusal (*"I have not publicly expressed a clear position on this matter..."*).
   - **Post-2015 Event Handling**: Queries regarding events after Lee Kuan Yew's lifetime (March 2015) are detected via regular expressions and keyword scanners, automatically prepending an explicit disclaimer: `"AN INFERENCE BASED ON HISTORICAL PRINCIPLES"`.

3. **Built-In LLM Evaluation Framework**:
   - The repository includes a evaluation framework (`app/evaluation/`) featuring a 60-query benchmark gold dataset.
   - Automated metrics evaluate Faithfulness, Persona Consistency, Citation Validity, and Refusal Precision using LLM-as-a-judge rubrics.

---

## 🔗 Live Production Deployment

* **Frontend App (Vercel)**: `https://lky-chatbot.vercel.app`
* **Backend API (Railway)**: `https://99-group-graduate-programlee-kuan-yew-chatbot-production.up.railway.app`
* **API Documentation**: `https://99-group-graduate-programlee-kuan-yew-chatbot-production.up.railway.app/docs`

---

## ⚡ Local Setup & Development Instructions

### Prerequisites
* **Node.js**: v18.0+ or v20.0+
* **Python**: v3.11+
* **Docker & Docker Compose** (Optional, for containerized local setup)

### Option A: Running via Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/ggerrio/99-Group-Graduate-Program_Lee-Kuan-Yew-Chatbot.git
cd 99-Group-Graduate-Program_Lee-Kuan-Yew-Chatbot

# 2. Copy environment file
cp .env.example .env
# Fill in your GEMINI_API_KEY in .env

# 3. Spin up backend container
docker-compose up --build
```
Backend server will be running at `http://localhost:8000`.

---

### Option B: Running Standalone (Localhost)

#### 1. Backend Setup (FastAPI)
```bash
# Navigate to project root and create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup (React / Vite)
```bash
# Install NPM packages
npm install

# Start Vite dev server
npm run dev
```
Frontend application will open at `http://localhost:3000` or `http://localhost:5173`.

---

## 🧪 Running Automated Tests & Evaluation

```bash
# Run pytest regression test suite
pytest app/tests/test_phase6_3_regression.py -v

# Run targeted 5-case regression harness
python -m app.evaluation.runners.run_phase6_3_regression

# Run full 60-query evaluation benchmark
python -m app.evaluation.runners.run_evaluation
```

---

## 💬 Recommended Questions to Try

The knowledge base currently covers four source documents: *The Singapore Story*, *From Third World to First*, *One Man's View of the World*, and *Singapore's Bilingual Journey* (see [Known Limitations](#-known-limitations--future-work) for scope details). The questions below are chosen to reliably demonstrate each of the system's core behaviors — grounded answers, honest refusal, and post-2015 inference labeling — using topics that are actually well-covered in the ingested corpus.

**Grounded, factual answers (should return a full response with citations):**
- "What were the core principles behind Singapore's economic success?"
- "What was the Graduate Mothers Scheme?"
- "Why did Lee Kuan Yew introduce bilingual education in Singapore?"
- "How does Lee Kuan Yew view meritocracy in governance?"
- "What is Lee Kuan Yew's perspective on China's rise as a global power?"
- "How did Lee Kuan Yew lead Singapore's transition from Third World to First?"

**Out-of-scope questions (should trigger a polite refusal, not a fabricated answer):**
- "What's your favorite recipe for chicken rice?"
- "How do I fix a leaking water pipe?"

**Post-2015 questions (should be explicitly labeled as inference, since Lee Kuan Yew passed away in March 2015):**
- "What would you think about ChatGPT and generative AI?"
- "What's your view on the COVID-19 pandemic response?"

Trying at least one question from each category is the fastest way to see the RAG grounding, refusal handling, and temporal-awareness features all working as designed.

---

## 📌 Known Limitations & Future Work

1. **Knowledge Corpus Scope**: Due to time constraints during development, only **4 source PDFs** were sourced and ingested — Lee Kuan Yew's two major memoirs (*The Singapore Story*, *From Third World to First*), one geopolitical essay collection (*One Man's View of the World*), and one article (*Singapore's Bilingual Journey*) — totaling **5,772 vector chunks**. The `knowledge/speeches/` and `knowledge/interviews/` directories are scaffolded in the ingestion pipeline (folder structure and pipeline support already exist) but are currently empty. Adding public-domain speech transcripts (e.g. National Day Rally speeches, parliamentary addresses) is the most direct way to expand corpus coverage, since the ingestion pipeline supports incremental additions without reprocessing existing documents.
2. **Evaluation Metrics Baseline**:
   - In the Phase 6.3 targeted regression benchmark over 5 previously failing queries, the system achieved **5/5 (100%) pass rate** (Faithfulness: `5.0/5.0`).
   - In the full 60-query Phase 6.1 baseline evaluation, overall faithfulness scored **87.5%**, with residual hallucinations occurring on broad synthesis queries. Refusal precision measured **42.8%** due to strict prefix-matching criteria.
3. **Session State**: Conversation history is maintained in-memory per session (`InMemoryChatHistoryManager`) and is not persisted to an external database.

---

## 👨‍💻 Author & Credits

* **Author**: Gerrio Pratama
* **Challenge**: *"What Would Lee Kuan Yew Do?"* AI Engineering Challenge
* **Submission Version**: `v1.0.0`