import asyncio
from fastapi import APIRouter, HTTPException
from app.locator_retrieval.locator_retrieving import LocatorRetrieving
from app.locator_retrieval.storage import db_locator


router = APIRouter()
@router.post("/scraper/start", tags=["locators"])
async def start_scraper_process(feature_id:int):
    scraper = LocatorRetrieving(feature_id)
    response = await scraper.scraper_process()
    return response

@router.get("/scraper/fetch_locators", tags=["locators"])
async def get_all_locators(feature_id: int):
    response = db_locator.get_selectors_by_feature(feature_id)
    return response

@router.get("/scraper/fetch_all_locator_data", tags=["locators"])
async def get_locator_element(feature_id: int):
    response = db_locator.get_all_locator_data_by_feature_id(feature_id)
    if response["status_code"] != 200:
        raise HTTPException(status_code=400, detail=response["message"])
    return response