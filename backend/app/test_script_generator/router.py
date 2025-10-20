from fastapi import APIRouter
from ..bdd_scenarios.storage import BDD_SCENARIOS
from app.requirement_handling.storage import REQUIREMENTS
from .storage import TEST_SCRIPTS
router = APIRouter()
@router.post("/test_scripts/generate",tags=["test_scripts"])
async def create_test(feature_id: int):
    retrieve_bdd_item = REQUIREMENTS[feature_id].get("bdd_scenarios")
    if retrieve_bdd_item.len() == 0:
        return f"Error: No bdd scenarios found for feature_id:{feature_id}"
    locators = {}
    #calls test generator
    #await testgen(retrieve_bdd_item, locators)
    generated_test = "Generated code here"
    id = len(TEST_SCRIPTS)+1
    TEST_SCRIPTS[id]={"id":id,"feature_id":feature_id,"content":generated_test}
    return "Test scripts generated successfully"
    
@router.get("/test_scripts",tags=["test_scripts"])
async def fetch_test(test_item_id: int):
    test_item = TEST_SCRIPTS[test_item_id]
    return test_item