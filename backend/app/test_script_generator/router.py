from fastapi import APIRouter, HTTPException
import time
from datetime import timedelta, datetime
import asyncio
import traceback
from fastapi.responses import JSONResponse
from app.requirement_handling.storage import db_requirements,URL_DATA
from app.locator_retrieval.storage import db_locator
from app.locator_retrieval.router import start_scraper_process
from app.bdd_scenarios.storage import db_bdd_scenarios
from .storage import db_test_scripts
from app.test_script_generator.script_gen import ScriptGen
router = APIRouter()
@router.post("/test_scripts/generate",tags=["test_scripts"])
async def create_test(feature_id: int):
    process = ScriptGen()
    
    feature_data = db_requirements.get_feature_data_by_id(feature_id)
    if not feature_data:
        return f"Feature not found with id:{feature_id}"
    bdd_scenarios= db_bdd_scenarios.get_all_bdd_scenarios_by_feature(feature_id)
    if not bdd_scenarios:
        return f"Error: No bdd scenarios found for feature_id:{feature_id}"
    locators = db_locator.get_selectors_by_feature(feature_id)
    if not locators:
        return JSONResponse(status_code=400, content={"error": "Locators not found"})
      
    login = {"username": URL_DATA.username,"password": URL_DATA.password}
    url = URL_DATA.url
    result = await process.generate_script([feature_data],bdd_scenarios,locators, login, url)
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    response = db_test_scripts.save_testscript(feature_id=feature_id,
                                    bdd_scenarios=bdd_scenarios,script_code=result["body"]
                                    )
    if response["status_code"] != 200:
        raise HTTPException(status_code=response["status_code"],detail=response["detail"])
    return {"status_code": 200, "detail": f"{result["detail"]}","body": f"{result["body"]}"}
    
@router.get("/test_scripts",tags=["test_scripts"])
async def fetch_test(feature_id: int):
    response = db_test_scripts.get_test_script_by_feature_id(feature_id)
    return response