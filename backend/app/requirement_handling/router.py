
import json
from fastapi import APIRouter, UploadFile, Form, File
from .schemas import Req_Process
from .storage import REQ_TOPICS, REQUIREMENTS
router = APIRouter()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics():
    return REQUIREMENTS
#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(json_item:str = Form(...), file: UploadFile = File(...)):
    #TODO: call requ processing phase to get features/tson(),opics with json_item and file
    parsed = json.loads(json_item)
    topics = ["login", "filter", "basket"]
    global REQ_TOPICS
    REQ_TOPICS = topics
    print(REQ_TOPICS)
    return {"message": "Requirements processed"}
