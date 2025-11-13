from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.common.database import get_session
from app.common.models.bdd_model import BDDScenario
from app.bdd_scenarios.schemas import BDD_Scenario
from .storage import db_bdd_scenarios
from .bdd_generation import generate_bdd_scenarios_logic 
router = APIRouter()

@router.get("/bdd_scenarios", tags=["bdd_scenarios"])
async def read_bdd_scenarios_by_feature(feature_id:int):
    bdds = db_bdd_scenarios.get_all_bdd_scenarios_by_feature(feature_id=feature_id)
    return bdds

@router.delete("/bdd_scenarios", tags=["bdd_scenario"])
async def delete_bdd_scenario_by_id(feature_id:int,bdd_id: int):
    response = db_bdd_scenarios.delete_bdd_scenario_by_id(feature_id,bdd_id)
    return response

@router.put("/bdd_scenarios", tags=["bdd_scenarios"])
async def update_bdd_scenario(feature_id: int,bdd_id:int,item: BDD_Scenario):
    
    response = db_bdd_scenarios.update_bdd_scenario_by_id(feature_id,bdd_id, item)
    return response


@router.post("/bdd_scenarios", tags=["bdd_scenarios"])
async def create_bdd_scenario(feature_id:int,item: BDD_Scenario):
    response = db_bdd_scenarios.add_bdd_scenarios(feature_id,item)
    return response

@router.post("/bdd_scenarios/generate/{id}", tags=["bdd_scenarios"])
async def generate_bdd_scenarios(id: int, session: Session = Depends(get_session)):
    
    generated_bdds = await generate_bdd_scenarios_logic(id)

    return {"message": "BDDs generated successfully"}


