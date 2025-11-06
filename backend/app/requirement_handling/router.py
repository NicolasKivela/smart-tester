
from fastapi import APIRouter, Depends, HTTPException,Form, UploadFile, File
from sqlmodel import Session, select
from app.common.database import get_session
from app.common.models.req_model import Processed_Req
import json
from .storage import REQ_TOPICS, REQUIREMENTS
from .agents import RequirementAgent
from .service import RequirementsProcessor
from .file_handler import extract_text

router = APIRouter()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics(session: Session = Depends(get_session)):
    requirements = session.exec(select(Processed_Req)).all()
    return requirements
#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(json_item:str = Form(...), 
                               file: UploadFile = File(...),
                               session: Session = Depends(get_session)):
    content = await file.read()
    text = extract_text(content,file.filename)
    json_item = json.loads(json_item)
    process=RequirementsProcessor(json_item, text, req_file=file)
    await process.run_pipeline()
    return {
        "message": "Requirements processed and saved",
    }
