from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
import os
import stat
DATABASE_URL = "sqlite:///app/database.db"  

engine = create_engine(DATABASE_URL, echo=True)  

def init_db():
    from app.common.models.req_model import Feature, RequirementDocument,Requirement
    from app.common.models.bdd_model import BDDScenario
    from app.common.models.locator_model import LocatorElements
    from app.common.models.test_script_model import TestScript
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.post("/database/reset", tags=["database"]) 
async def reset_database():
    try:
        db_path = DATABASE_URL.replace("sqlite:///", "")

        # Ensure directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        engine.dispose()

        if os.path.exists(db_path):
            os.remove(db_path)

        # Reset logs
        from app.common.logs.logger_config import reset_logs
        from app.common.token_logging.service import reset_token_logs
        reset_logs()
        reset_token_logs()

        init_db()

        # Fix permissions for Docker
        os.chmod(db_path, 0o666) 
        return {"status": "200", "message": "Database successfully reset"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 