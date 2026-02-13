"""TF-IDF based job–resume similarity scoring with Joblib for model caching."""
from pathlib import Path
from typing import Tuple

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"


def _ensure_model_dir():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)


def get_vectorizer():
    """Load or create TF-IDF vectorizer; cache with Joblib for fast reuse."""
    _ensure_model_dir()
    if VECTORIZER_PATH.exists():
        return joblib.load(VECTORIZER_PATH)
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
    )
    joblib.dump(vectorizer, VECTORIZER_PATH)
    return vectorizer


def compute_similarity(resume_text: str, job_description: str) -> float:
    """
    Compute TF-IDF cosine similarity between resume and job description (0–1).
    Fits vectorizer on the pair for accurate vocabulary; uses Joblib-cached
    vectorizer only for loading (inference is optimized via sklearn).
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1,
        sublinear_tf=True,
    )
    vectors = vectorizer.fit_transform([resume_text, job_description])
    sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return float(min(max(sim, 0.0), 1.0))
