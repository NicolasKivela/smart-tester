import re
import io
import pdfplumber
from docx import Document



def extract_text(file_bytes: bytes, filename: str):
    # Extract text from PDF, DOCX, or TXT file.
    if filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join(p.text for p in doc.paragraphs)

    elif filename.endswith(".txt"):
        text = file_bytes.decode("utf-8")

    else:
        raise ValueError("Unsupported file type")

    return clean_text(text)
def clean_text(text):
    # Basic cleaning for whitespace and line breaks.

    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()