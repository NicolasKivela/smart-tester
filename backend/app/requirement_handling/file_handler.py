import re
import pdfplumber
from docx import Document



def extract_text(file_path):
    # Extract text from PDF, DOCX, or TXT file.

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    else:
        raise ValueError("Unsupported file type")
    return clean_text(text)

def clean_text(text):
    # Basic cleaning for whitespace and line breaks.

    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()