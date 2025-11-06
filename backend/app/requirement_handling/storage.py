# temporary storage
from sqlmodel import Session, select
from app.common.database import engine
from app.common.models.req_model import Processed_Req,Extracted_Reqs
from app.common.models.bdd_model import BDDScenario
from app.requirement_handling.schemas import UrlCredentials, Credentials
import re

# Optional: keep memory cache for speed / backward compatibility
REQUIREMENTS: dict[int, Processed_Req] = {}
REQ_TOPICS = []
URL_DATA = UrlCredentials(url="https://www.hsl.fi/", credentials=Credentials(username="", password=""))

class db_requirements:
    @staticmethod
    def get_req_by_id(id: int):
        if id in REQUIREMENTS:
            return REQUIREMENTS[id]
        with Session(engine) as session:
            req = session.get(Processed_Req, id)
            if req:
                REQUIREMENTS[id] = req
            return req

    @staticmethod
    def add_bdd_scenarios(feature_id: int, bdd_scenario: dict):
        with Session(engine) as session:
            req = session.get(Processed_Req, feature_id)
            if not req:
                print(f"Requirement {feature_id} not found")
                return

            new_bdd = BDDScenario(**bdd_scenario, processed_req_id=feature_id)
            session.add(new_bdd)
            session.commit()
            session.refresh(req)

            REQUIREMENTS[feature_id] = req
            return "BDD scenario added successfully"

    @staticmethod
    def create_processed_req(processed_reqs: dict, summaries: dict, topics: dict):
        with Session(engine) as session:
            for i, (key, value) in enumerate(processed_reqs.items(), start=1):
                processed = Processed_Req(
                    feature=key,
                    summary=re.sub(r'^\*\*Topic:.*?\*\*\s*', '', summaries.get(key, ""), flags=re.MULTILINE),
                    requirements=Extracted_Reqs(topics_reqs=value),
                )
                session.add(processed)
                session.commit()
                session.refresh(processed)
                REQUIREMENTS[processed.id] = processed
                print("data stored to session")
            return "Processed requirements created successfully"

    @staticmethod
    def save_url_data(url, credentials):
        global URL_DATA
        try:
            URL_DATA = UrlCredentials(url=url, credentials=credentials)
            return "URL data saved successfully"
        except Exception as e:
            print("Error saving URL data:", e)
            return None
