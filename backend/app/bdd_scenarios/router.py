from fastapi import APIRouter
from .schemas import BDD_Scenario, Generate_BDD
from .storage import BDD_SCENARIOS
router = APIRouter()

@router.get("/bdd_scenarios",tags=["bdd_scenarios"])
async def read_bdd_scenarios():
    return BDD_SCENARIOS

@router.put("/bdd_scenarios/{id}",tags=["bdd_scenarios"])
async def update_bdd_scenario(item_id: int, item: BDD_Scenario):
    BDD_SCENARIOS[item.id] = item.model_dump()
    return {"message": "Item replaced", "id":item_id}

@router.post("/bdd_scenarios/",tags=["bdd_scenarios"])
async def create_bdd_scenario(item: BDD_Scenario):
    BDD_SCENARIOS[item.id]=item.model_dump()
    return {"message": "Item created" , "id":item.id}

#Generate BDD_scenarios
@router.post("/bdd_scenarios",tags=["bdd_scenarios"])
async def generate_bdd_scenarios(item: Generate_BDD):
    #TODO: Call async generator model
    #async generator(item)
    generated_bdds = [{"id": len(BDD_SCENARIOS)+1, 
                       "feature": item.feature, 
                       "scenario": "Scenario here", 
                       "given": ["given that","given that"], 
                       "when": ["this","that"], 
                       "then": ["then this"]}]

    for bdd in generated_bdds:
        bdd_obj = BDD_Scenario(**bdd)
        print(bdd)
        BDD_SCENARIOS[bdd_obj.id]= bdd
    return {"message": "BDDs generated succesfully"}



