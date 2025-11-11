from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.common.database import get_session
from .schemas import BDD_Scenario, Generate_BDD
from app.common.models.bdd_model import BDDScenario
from app.requirement_handling.service import get_requirements
from .storage import BDD_SCENARIOS, db_bdd_scenarios
from .bdd_generation import generate_bdd_scenarios_logic 
from app.requirement_handling.storage import REQUIREMENTS
router = APIRouter()

@router.get("/bdd_scenarios", tags=["bdd_scenarios"])
async def read_bdd_scenarios_by_feature(feature_id:int):
    bdds = db_bdd_scenarios.get_all_bdd_scenarios_by_feature(feature_id=feature_id)
    return bdds

@router.delete("/bdd_scenarios", tags=["bdd_scenario"])
async def delete_bdd_scenario_by_id(bdd_id: int):
    response = db_bdd_scenarios.delete_bdd_scenario_by_id(bdd_id)
    return response

@router.put("/bdd_scenarios", tags=["bdd_scenarios"])
async def update_bdd_scenario(id: int, item: BDDScenario):
    
    response = db_bdd_scenarios.update_bdd_scenario_by_id(id, item)
    return response


@router.post("/bdd_scenarios", tags=["bdd_scenarios"])
async def create_bdd_scenario(item: BDDScenario):
    response = db_bdd_scenarios.add_bdd_scenarios(item.feature_id,item)
    return response

@router.post("/bdd_scenarios/generate/{id}", tags=["bdd_scenarios"])
async def generate_bdd_scenarios(id: int, session: Session = Depends(get_session)):
    
    generated_bdds = await generate_bdd_scenarios_logic(id)

    return {"message": "BDDs generated successfully", "count": len(generated_bdds)}


