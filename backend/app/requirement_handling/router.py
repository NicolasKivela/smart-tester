"""
API routes for handling requirement documents.

This module exposes endpoints to:
- Fetch stored requirement topics and related data from the database.
- Upload and process a new requirement document (plus optional URL credentials),
  run it through the requirements processing pipeline, and store the results.

The actual storage and processing logic is delegated to:
- `db_requirements` for database interactions.
- `RequirementsProcessor` for LLM-based analysis and extraction.
- `extract_text` for parsing raw file content into plain text.
"""
from typing import Optional
from fastapi import APIRouter,Form, UploadFile, File
from app.common.database import get_session
from .schemas import UrlCredentials
import json
from .storage import db_requirements
from .service import RequirementsProcessor
from .file_handler import extract_text

router = APIRouter()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics():
    response = db_requirements.get_all_feature_data()
    return response
#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(url: str = Form(...),
                                username: Optional[str] = Form(None),
                                password: Optional[str] = Form(None), 
                               file: UploadFile = File(...)):
    credentials = UrlCredentials(
        username=username,
        password=password
    )
    content = await file.read()
    text = extract_text(content,file.filename)
    session_id = "full_session"
    process=RequirementsProcessor(url,credentials, text, req_file=file.filename, session_id=session_id)
    response = await process.run_pipeline()
    
    return response
