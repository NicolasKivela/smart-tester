from fastapi import APIRouter, Response
import os

router = APIRouter()

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "files", "ai_agent.log")

@router.get("/logs/ai-agent", tags=["logs"])
async def get_ai_agent_logs():
    """
    Returns the whole log file (downloadable from the front end)
    """
    if not os.path.exists(LOG_FILE_PATH):
        return {"error": "Log file not found"}

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    return Response(content, media_type="text/plain")