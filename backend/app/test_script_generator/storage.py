import json
from sqlmodel import select
from app.common.database import Session, engine
from app.test_script_generator.schemas import test_script
from app.common.models import BDDScenario, LocatorElements
from app.common.models.test_script_model import TestScript

class db_test_scripts():
    def save_keywords(id):
        return
    def get_keywords():
        return
    def save_testscript(feature_id, bdd_scenarios,script_code):
        try:
            with Session(engine) as session:
                test_script = TestScript(feature_id=feature_id, script_code=script_code)
                session.add(test_script)
                session.flush()
                script_id = test_script.id
                scenarios = session.exec(
                    select(BDDScenario).where(BDDScenario.feature_id == feature_id)
                ).all()
                for sc in scenarios:
                    sc.test_script_id = test_script.id

                locators = session.exec(
                    select(LocatorElements).where(LocatorElements.feature_id == feature_id)
                ).all()
                for loc in locators:
                    loc.test_script_id = test_script.id

                session.commit()
            return {"status_code":200,"detail":"Succesfully saved test script object"}
        except Exception as e:
            print(f"error {e}")
            print(f"Error saving testscript id:{id}")  
            return {"status_code":400,"detail": "Error when saving test script to database"}
    def get_test_script_by_feature_id(feature_id):
        try:
            with Session(engine) as session:
                test_script = session.exec(
                    select(TestScript).where(TestScript.feature_id == feature_id)
                ).all()
                return {"status_code":200,"body":test_script}
        except Exception as e:
            return {"status_code": 400, "message": "Error fetching test script"}