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
async def read_bdd_scenarios(session: Session = Depends(get_session)):
    bdds = session.exec(select(BDDScenario)).all()
    return bdds

@router.put("/bdd_scenarios/{id}", tags=["bdd_scenarios"])
async def update_bdd_scenario(id: int, item: BDDScenario, session: Session = Depends(get_session)):
    db_item = session.get(BDDScenario, id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"BDDScenario with id={id} not found")

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"message": "Item updated", "id": db_item.id}


@router.post("/bdd_scenarios", tags=["bdd_scenarios"])
async def create_bdd_scenario(item: BDDScenario, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return {"message": "Item created", "id": item.id}

@router.post("/bdd_scenarios/generate/{id}", tags=["bdd_scenarios"])
async def generate_bdd_scenarios(id: int, session: Session = Depends(get_session)):
    requirement_item = get_requirements(id)
    generated_bdds = await generate_bdd_scenarios_logic(requirement_item)

    for bdd in generated_bdds:
        db_bdd = BDDScenario(**bdd.model_dump())
        session.add(db_bdd)

    session.commit()
    return {"message": "BDDs generated successfully", "count": len(generated_bdds)}


