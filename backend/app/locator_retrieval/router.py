from fastapi import APIRouter
from app.locator_retrieval.locator_retrieving import LocatorRetrieving


router = APIRouter()
@router.post("/scraper/start", tags=["scraper"])
async def start_scraper_process(feature_id):
    service = LocatorRetrieving(feature_id)
    service.locator_retrieving_service()

    return 