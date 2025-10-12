
import json
from fastapi import APIRouter, UploadFile, Form, File
from .schemas import Req_Process, Req_Topics
from .storage import REQ_TOPICS
from .agents import RequirementAgent
import json

router = APIRouter()
agent = RequirementAgent()

#Get requirement file features
@router.get("/requirements", tags=["requirements"])
async def fetch_requirement_topics():
    return REQ_TOPICS

#Process requirements
@router.post("/requirements",tags=["requirements"])
async def process_requirements(json_item:str = Form(...), file: UploadFile = File(...)):
    parsed = json.loads(json_item)
    # Save file temporarily
    content = await file.read()
    with open("temp_input.txt", "wb") as f:
        f.write(content)

    # Use BaseAgent to process the document
    text = None
    with open("temp_input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    topics = agent.execute_task(f"Detect topics in the document:\n{text}")
    REQ_TOPICS.clear()
    REQ_TOPICS.extend(topics if isinstance(topics, list) else [topics])

    # Summaries
    summaries = {}
    for topic in REQ_TOPICS:
        summary = agent.execute_task(f"Summarize the document for topic '{topic}':\n{text}")
        summaries[topic] = summary
        save_to_file("output", f"{topic}_summary.txt", summary)

    # Detailed requirements
    for topic in REQ_TOPICS:
        requirements = agent.execute_task(f"Extract detailed requirements for topic '{topic}':\n{text}")
        save_to_file("output", f"{topic}_requirements.json", requirements)

    return {"message": "Requirements processed", "topics": REQ_TOPICS}