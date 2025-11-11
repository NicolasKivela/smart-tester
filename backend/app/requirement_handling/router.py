
from fastapi import APIRouter, Depends, HTTPException,Form, UploadFile, File
from sqlmodel import Session, select
from app.common.database import get_session
from .schemas import Credentials, UrlCredentials
import json
from .storage import REQ_TOPICS, REQUIREMENTS, db_requirements
from .agents import RequirementAgent
from .service import RequirementsProcessor
from .file_handler import extract_text

router = APIRouter()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics(session: Session = Depends(get_session)):
    all_feature_data = db_requirements.get_all_feature_data()
    feature_names = []
    for feature in all_feature_data:
        feature_names.append(feature.name)
    return feature_names
#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(form_item: str = Form(...), 
                               file: UploadFile = File(...),
                               session: Session = Depends(get_session)):
    print(form_item)
    credentials = UrlCredentials(**json.loads(form_item))
    print(credentials)
    content = await file.read()
    text = extract_text(content,file.filename)
    process=RequirementsProcessor(credentials, text, req_file=file.filename)
    await process.run_pipeline()
    return {
        "message": "Requirements processed and saved",
    }
