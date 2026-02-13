"""ResumeN — FastAPI backend for AI Resume Analyzer."""
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.pdf_parser import extract_text_from_pdf
from app.similarity import compute_similarity
from app.skill_extractor import extract_skills

app = FastAPI(
    title="ResumeN — AI Resume Analyzer",
    description="NLP-based resume analysis with TF-IDF job–resume similarity and spaCy skill extraction.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeTextRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalyzeTextResponse(BaseModel):
    similarity_score: float
    similarity_percent: float
    skills: List[str]
    resume_preview: str


class AnalyzePdfResponse(BaseModel):
    similarity_score: float
    similarity_percent: float
    skills: List[str]
    resume_text: str
    resume_preview: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "ResumeN"}


@app.post("/api/analyze/text", response_model=AnalyzeTextResponse)
def analyze_text(req: AnalyzeTextRequest):
    """Analyze resume and job description from raw text."""
    score = compute_similarity(req.resume_text, req.job_description)
    skills = extract_skills(req.resume_text)
    preview = (req.resume_text[:500] + "...") if len(req.resume_text) > 500 else req.resume_text
    return AnalyzeTextResponse(
        similarity_score=round(score, 4),
        similarity_percent=round(score * 100, 2),
        skills=skills,
        resume_preview=preview,
    )


@app.post("/api/analyze/pdf", response_model=AnalyzePdfResponse)
async def analyze_pdf(
    file: UploadFile = File(...),
    job_description: str = Form(""),
):
    """Parse PDF resume and analyze against job description. Send job_description as form field."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file.")
    resume_text = extract_text_from_pdf(content)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    job_description = job_description or "Software development, programming, technical skills."
    score = compute_similarity(resume_text, job_description)
    skills = extract_skills(resume_text)
    preview = (resume_text[:500] + "...") if len(resume_text) > 500 else resume_text
    return AnalyzePdfResponse(
        similarity_score=round(score, 4),
        similarity_percent=round(score * 100, 2),
        skills=skills,
        resume_text=resume_text,
        resume_preview=preview,
    )


class SkillsRequest(BaseModel):
    resume_text: str


@app.post("/api/skills")
def extract_skills_from_text(req: SkillsRequest):
    """Extract skills from resume text only."""
    return {"skills": extract_skills(req.resume_text)}
