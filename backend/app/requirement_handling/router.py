import json
from fastapi import APIRouter, UploadFile, Form, File
from .storage import REQ_TOPICS, REQUIREMENTS
from .agents import RequirementAgent
from .service import RequirementsProcessor
from .file_handler import extract_text

router = APIRouter()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics():
    return REQUIREMENTS
#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(json_item:str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(content,file.filename)
    process=RequirementsProcessor(json_item, text, req_file=file)
    process.run_pipeline()
    topics = process.topics
    print("processing", REQUIREMENTS)
    return {"message": "Requirements processed", "Requirements": REQUIREMENTS}
