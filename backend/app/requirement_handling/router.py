
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException,Form, UploadFile, File
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
    print("ROUTEER CALLED PROCESSING")
    content = await file.read()
    text = extract_text(content,file.filename)
    session_id = "full_session"
    process=RequirementsProcessor(url,credentials, text, req_file=file.filename, session_id=session_id)
    print(process)
    response = await process.run_pipeline()
    
    return response



