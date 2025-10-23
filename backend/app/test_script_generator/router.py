from fastapi import APIRouter
from ..bdd_scenarios.storage import BDD_SCENARIOS
from app.requirement_handling.storage import db_requirements
from .storage import TEST_SCRIPTS, db_test_scripts
from app.test_script_generator.script_gen import ScriptGen
router = APIRouter()
@router.post("/test_scripts/generate",tags=["test_scripts"])
async def create_test(feature_id: int):
    process = ScriptGen()
    
    feature_data = db_requirements.get_req_by_id(feature_id)
    if not feature_data:
        return f"Feature not found with id:{feature_id}"
    bdd_scenarios= feature_data.bdd_scenarios
    if not bdd_scenarios:
        return f"Error: No bdd scenarios found for feature_id:{feature_id}"
    locators = {}
    login = {}
    result = process.generate_script([feature_data], locators, login)
    id = len(TEST_SCRIPTS)+1
    db_test_scripts.save_testscript(id, feature_id=feature_id,
                                    bdd_scenarios=bdd_scenarios,script_code=result
                                    )
    return result
    
@router.get("/test_scripts",tags=["test_scripts"])
async def fetch_test(test_item_id: int):
    test_item = TEST_SCRIPTS[test_item_id]
    return test_item