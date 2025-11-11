import asyncio
from fastapi import APIRouter
from app.locator_retrieval.locator_retrieving import LocatorRetrieving
from app.locator_retrieval.storage import LOCATORS


router = APIRouter()
@router.post("/scraper/start", tags=["scraper"])
async def start_scraper_process(feature_id:int):
    scraper = LocatorRetrieving(feature_id)
    response = await asyncio.create_task(scraper.scraper_process())
    return response

@router.get("/scraper/fetch_locators", tags=["locators"])
async def get_all_locators():
    return LOCATORS