from fastapi import APIRouter
from .schemas import BDD_Scenario, Generate_BDD
from app.requirement_handling.service import get_requirements
from .storage import BDD_SCENARIOS
from .bdd_generation import generate_bdd_scenarios_logic 
from app.requirement_handling.storage import REQUIREMENTS
router = APIRouter()

@router.get("/bdd_scenarios",tags=["bdd_scenarios"])
async def read_bdd_scenarios():
    return BDD_SCENARIOS

@router.put("/bdd_scenarios/{id}",tags=["bdd_scenarios"])
async def update_bdd_scenario(item_id: int, item: BDD_Scenario):
    BDD_SCENARIOS[item.id] = item.model_dump()
    return {"message": "Item replaced", "id":item_id}

@router.post("/bdd_scenarios",tags=["bdd_scenarios"])
async def create_bdd_scenario(item: BDD_Scenario):
    BDD_SCENARIOS[item.id]=item.model_dump()
    return {"message": "Item created" , "id":item.id}

#Generate BDD_scenarios
@router.post("/bdd_scenarios/generate/{id}",tags=["bdd_scenarios"])
async def generate_bdd_scenarios(item_id:int):
    requirement_item = get_requirements(item_id) 
    generated_bdds = await generate_bdd_scenarios_logic(requirement_item) 

    for bdd in generated_bdds:
        print(bdd)
        BDD_SCENARIOS[bdd.id]= bdd.model_dump()
        REQUIREMENTS[item_id]=BDD_SCENARIOS[bdd.id]
    return {"message": "BDDs generated succesfully", "generated_scenarios": generated_bdds}


