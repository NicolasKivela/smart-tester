from fastapi import APIRouter
from .schemas import BDD_Scenario, Generate_BDD
from .storage import BDD_SCENARIOS
from .bdd_generation import generate_bdd_scenarios_logic 
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
@router.post("/bdd_scenarios/generate",tags=["bdd_scenarios"])
async def generate_bdd_scenarios(item: Generate_BDD):
    
    generated_bdds = await generate_bdd_scenarios_logic(item) 

    for bdd in generated_bdds:
        print(bdd)
        BDD_SCENARIOS[bdd.id]= bdd.model_dump()
    return {"message": "BDDs generated succesfully", "generated_scenarios": generated_bdds}


