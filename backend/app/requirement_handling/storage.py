# temporary storage
import logging
from sqlmodel import Session, select
from app.common.database import engine
from app.common.models.req_model import Requirement,RequirementDocument,Feature
from app.common.models.bdd_model import BDDScenario
from app.requirement_handling.schemas import UrlCredentials, Credentials
import re

# Optional: keep memory cache for speed / backward compatibility
REQUIREMENTS: dict[int, Feature] = {}
REQ_TOPICS = []
URL_DATA = UrlCredentials(url="https://www.hsl.fi/",username="", password="")

class db_requirements:
    @staticmethod
    def get_feature_data_by_id(id: int):
        if id in REQUIREMENTS:
            return REQUIREMENTS[id]
        with Session(engine) as session:
            req = session.get(Feature, id)
            if req:
                REQUIREMENTS[id] = req
            print(req)
            return req
    @staticmethod
    def get_all_feature_data():
        with Session(engine) as session:
            features = session.exec(select(Feature)).all()
        return features 
    @staticmethod
    def add_bdd_scenarios(feature_id: int, bdd_scenario: dict):
        with Session(engine) as session:
            req = session.get(Feature, feature_id)
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
    def save_requirement_document(document_name, raw_text):
        try:
            with Session(engine) as session:
                doc = RequirementDocument(document_name=document_name,raw_text=raw_text)
                session.add(doc)
                session.commit()
                session.refresh(doc)
                logging.info("Requirement document saved succesfully")
                return doc.id
            
        except Exception as e:
            logging.exception("saving requirement document error")


    @staticmethod
    def create_processed_req(processed_reqs: dict, summaries: dict, topics: dict, doc_id: int):
        try:
            with Session(engine) as session:
                doc = session.get(RequirementDocument, doc_id)
                if not doc:
                    logging.exception("When creating processed requirements data: Requirement document not found in database")
                    return "error"
                for i, (feature_name, req_texts) in enumerate(processed_reqs.items(), start=1):
                    print(summaries)
                    feature = Feature(name=feature_name, summary=summaries.get(feature_name))
                    i = 0
                    for req in req_texts:
                        identifier = f"{feature_name[:3].upper()}-{i}"
                        requirement = Requirement(identifier=identifier,text=req,feature=feature, document=doc)
                        session.add(requirement)
                    session.add(feature)
                session.commit()
                return "Processed requirements created successfully"
        except Exception as e:
            logging.exception("Error when creating processed reqs:")
            return e
            

    @staticmethod
    def save_url_data(url, credentials):
        global URL_DATA
        try:
            URL_DATA = UrlCredentials(url=url, credentials=credentials)
            return "URL data saved successfully"
        except Exception as e:
            print("Error saving URL data:", e)
            return None
