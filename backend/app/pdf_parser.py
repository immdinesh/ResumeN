"""PDF parsing for resume text extraction."""
import io
from pathlib import Path

import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from a PDF file."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text_parts.append(extracted)
    return "\n".join(text_parts).strip() if text_parts else ""
