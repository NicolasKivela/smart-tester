import logging
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.common.database import engine
from app.requirement_handling.storage import db_requirements
from app.common.models import BDDScenario, Requirement, Feature
from app.bdd_scenarios.schemas import BDD_Scenario

BDD_SCENARIOS ={}

class db_bdd_scenarios():
    def add_bdd_scenarios(feature_id,bdd_scenario: BDD_Scenario):
        try:
            with Session(engine) as session:
                req = session.get(Feature, feature_id)
                if not req:
                    print(f"Requirement {feature_id} not found")
                    return {"status_code": 404, "message": f"Requirement {feature_id} not found"}
                db_bdd = BDDScenario(**bdd_scenario.model_dump())
                db_bdd.feature_id = feature_id
                session.add(db_bdd)
                session.commit()
                session.refresh(db_bdd)

                return {"status_code":200, "message": "BDD scenario added successfully","id":db_bdd.id,}
        except Exception as e:
            return {"status_code":400,"message": f"Error saving bdd_scenarios: {e}"}

    def get_bdd_scenario_by_id(bdd_id):
        with Session(engine) as session:
            statement = (
                select(BDDScenario)
                .where(BDDScenario.id == bdd_id)
            )
            bdd_scenario = session.exec(statement).first()

            return bdd_scenario
    def get_all_bdd_scenarios_by_feature(feature_id):
        with Session(engine) as session:
            statement=(
                select(BDDScenario)
                .where(BDDScenario.feature_id ==feature_id)
            )
            bdds = session.exec(statement).all()
            return bdds
    def delete_bdd_scenario_by_id(feature_id,bdd_id):
        with Session(engine) as session:

            statement = (select(BDDScenario)
                         .where(BDDScenario.feature_id==feature_id,
                                BDDScenario.id == bdd_id))
            bdd = session.execute(statement).scalar_one_or_none()
            if not bdd:
                return {"status_code":404,"message":f"Bdd with id: {bdd_id} not found"}
            session.delete(bdd)
            session.commit()
            return {"status_code":200,"message":f"Bdd scenario deleted with id:{bdd_id}"}
    def update_bdd_scenario_by_id(feature_id,bdd_id,updated_item):
        with Session(engine) as session:
            statement = (select(BDDScenario)
                         .where(BDDScenario.feature_id==feature_id,
                                BDDScenario.id == bdd_id))
            db_item = session.execute(statement).scalar_one_or_none()
            if not db_item:
                return {"status_code":404, "message":f"BDDScenario with id={id} not found"}

            for key, value in updated_item.model_dump(exclude_unset=True,exclude={"id","feature_id","locator_element_id","test_script_id"}).items():
                setattr(db_item, key, value)

            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return {"status_code":200,"message": "Item updated", "id": db_item.id}