"""Skill extraction using spaCy NER and keyword matching."""
import re
from pathlib import Path
from typing import List, Set

# Common tech and soft skills for matching (expand as needed)
SKILL_KEYWORDS = {
    "python", "java", "javascript", "typescript", "react", "node", "node.js",
    "fastapi", "django", "flask", "sql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "git", "ci/cd",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "spacy", "tf-idf", "rest api", "graphql",
    "html", "css", "sass", "redux", "vue", "angular", "agile", "scrum",
    "leadership", "communication", "problem solving", "team collaboration",
    "data analysis", "data science", "etl", "spark", "hadoop",
    "figma", "ui/ux", "testing", "jest", "pytest", "tdd", "oop",
}


def _load_nlp():
    """Lazy-load spaCy model for faster startup."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        import spacy
        nlp = spacy.load("en_core_web_sm")
    return nlp


_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = _load_nlp()
    return _nlp


def extract_skills_spacy(text: str) -> List[str]:
    """Extract skills using spaCy NER (ORG, PRODUCT, etc.) and noun chunks."""
    nlp = get_nlp()
    doc = nlp(text[:100000])  # limit length
    skills: Set[str] = set()

    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT", "GPE", "WORK_OF_ART"):
            skill = ent.text.strip().lower()
            if len(skill) > 1 and len(skill) < 50:
                skills.add(skill)

    for chunk in doc.noun_chunks:
        chunk_lower = chunk.text.strip().lower()
        if 2 <= len(chunk_lower) <= 40 and chunk_lower not in {"i", "we", "my", "the"}:
            skills.add(chunk_lower)

    return sorted(skills)


def extract_skills_keywords(text: str) -> List[str]:
    """Extract skills by matching against a known skill keyword set."""
    text_lower = text.lower()
    found = set()
    for kw in SKILL_KEYWORDS:
        if kw in text_lower:
            found.add(kw)
    return sorted(found)


def extract_skills(text: str) -> List[str]:
    """Combine spaCy and keyword-based skill extraction."""
    by_keyword = set(extract_skills_keywords(text))
    by_spacy = set(extract_skills_spacy(text))
    combined = by_keyword | by_spacy
    return sorted(combined)
