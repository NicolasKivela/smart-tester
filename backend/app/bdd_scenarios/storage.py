#temporary
from app.requirement_handling.storage import db_requirements

BDD_SCENARIOS ={}

class db_bdd_scenarios():
    def add_bdd_scenarios(feature_id,bdd_scenario):
        db_requirements.add_bdd_scenarios(feature_id,bdd_scenario=bdd_scenario)