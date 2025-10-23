#temporary
from app.requirement_handling.storage import db_requirements

BDD_SCENARIOS ={}

class db_bdd_scenarios():
    def save_bdd_scenarios(id,bdd_scenarios):
        db_requirements.save_bdd_scenarios(id,bdd_scenarios=bdd_scenarios)