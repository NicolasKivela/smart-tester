from fastapi import APIRouter
from .schemas import BDD_Scenario

BDD_SCENARIOS ={}
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
    return {"message": "Item replaced", "id":item.id}



