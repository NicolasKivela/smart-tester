from fastapi import APIRouter, HTTPException
from app.common.token_logging.service import SESSION_TOKEN_LOGGERS

router = APIRouter()

@router.get("/token-logs/{session_id}")
def get_token_logs(session_id: str):
    logger = SESSION_TOKEN_LOGGERS.get(session_id)
    if not logger:
        raise HTTPException(status_code=404, detail="Session not found")
    return logger.get_summary()