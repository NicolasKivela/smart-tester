from fastapi import APIRouter
from ..bdd_scenarios.storage import BDD_SCENARIOS
from .storage import TEST_SCRIPTS
router = APIRouter()
@router.post("/test_scripts",tags=["test_scripts"])
async def create_test(bdd_item_id: int):
    retrieve_bdd_item = BDD_SCENARIOS[bdd_item_id]
    locators = {}
    #calls test generator
    #await testgen(retrieve_bdd_item, locators)
    generated_test = "Generated code here"   
    id = len(TEST_SCRIPTS)+1
    TEST_SCRIPTS[id]={"id":id,"bdd_id":bdd_item_id,"content":generated_test}
    return TEST_SCRIPTS
    
@router.get("/test_scripts",tags=["test_scripts"])
async def fetch_test(test_item_id: int):
    test_item = TEST_SCRIPTS[test_item_id]
    return test_item
