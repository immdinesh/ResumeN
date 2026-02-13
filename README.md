# ResumeN — AI Resume Analyzer

NLP-based resume analyzer with **TF-IDF** job–resume similarity scoring, **spaCy** skill extraction, **PDF** parsing, and a **FastAPI** backend with **React** frontend.

## Features

- **Job–resume similarity**: TF-IDF + cosine similarity for a 0–100% match score
- **Skill extraction**: Automated skills via spaCy NER and keyword matching
- **PDF parsing**: Resume text extraction from PDF uploads (pdfplumber)
- **Dual input**: Upload a PDF or paste resume text
- **Real-time analysis**: FastAPI + React with optional Joblib-cached models

## Requirements

- **Python 3.10–3.12** recommended (for scikit-learn/spaCy wheels; 3.14 may need build tools).
- Node.js 18+ for the frontend.

## Quick start

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. Use "Upload PDF" or "Paste text", optionally add a job description, and click **Analyze resume**.

## Project layout

```
ResumeN/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, /api/analyze/pdf, /api/analyze/text
│   │   ├── pdf_parser.py    # PDF text extraction (pdfplumber)
│   │   ├── skill_extractor.py  # spaCy + keyword skill extraction
│   │   └── similarity.py    # TF-IDF similarity (Joblib-ready)
│   ├── models/              # Optional: Joblib-saved vectorizer
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Upload/paste UI, results (score, skills, preview)
│   │   ├── api.ts          # analyzePdf(), analyzeText()
│   │   └── main.tsx
│   └── package.json
└── README.md
```

## API

- `POST /api/analyze/pdf` — `file` (PDF), `job_description` (form). Returns similarity, skills, resume text/preview.
- `POST /api/analyze/text` — JSON `{ resume_text, job_description }`. Same response shape.
- `GET /health` — Health check.

## Stack

- **Backend**: FastAPI, scikit-learn (TF-IDF), spaCy, pdfplumber, Joblib
- **Frontend**: React 18, Vite, TypeScript
