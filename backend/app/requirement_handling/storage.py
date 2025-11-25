# temporary storage
import logging
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.common.database import engine
from app.common.models.req_model import Requirement,RequirementDocument,Feature
from app.common.models.bdd_model import BDDScenario
from app.requirement_handling.schemas import UrlCredentials

# Optional: keep memory cache for speed / backward compatibility
REQUIREMENTS: dict[int, Feature] = {}
REQ_TOPICS = []
URL_DATA = UrlCredentials(username="", password="")

class db_requirements:
    @staticmethod
    def get_feature_data_by_id(id: int):
        if id in REQUIREMENTS:
            return REQUIREMENTS[id]

        with Session(engine) as session:
            statement = (
                select(Feature)
                .options(selectinload(Feature.requirements))
                .where(Feature.id == id)
            )
            feature = session.exec(statement).first()

            if feature:
                REQUIREMENTS[id] = feature
            return feature
    @staticmethod
    def get_all_feature_data():
        try:
            with Session(engine) as session:
                features = session.exec(select(Feature)).all()

            return features
        except Exception as e:
            return {"status_code": 400, "message": "Error fetching all feature data: {e}"}
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
    def save_requirement_document(document_name, raw_text, app_url):
        try:
            with Session(engine) as session:
                doc = RequirementDocument(document_name=document_name,raw_text=raw_text, app_url=app_url)
                session.add(doc)
                session.commit()
                session.refresh(doc)
                logging.info("Requirement document saved succesfully")
                return doc.id

        except Exception as e:
            logging.exception("saving requirement document error")


    @staticmethod
    def create_processed_req(processed_reqs: dict, summaries: dict, topics: dict, doc_id: int, app_url: str):
        try:
            with Session(engine) as session:
                doc = session.get(RequirementDocument, doc_id)
                if not doc:
                    logging.exception("When creating processed requirements data: Requirement document not found in database")
                    return "error"
                for i, (feature_name, req_texts) in enumerate(processed_reqs.items(), start=1):
                    feature = Feature(name=feature_name, summary=summaries.get(feature_name),app_url=app_url, requirement_document_id=doc_id)
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
    def save_credentials_data_local(credentials):
        global URL_DATA
        try:
            URL_DATA = UrlCredentials(credentials=credentials)
            return "URL data saved successfully"
        except Exception as e:
            print("Error saving URL data:", e)
            return None
    @staticmethod
    def get_credentials():
        global URL_DATA
        try:
            if URL_DATA is None:
                return None
            return URL_DATA
        except Exception as e:
            print("Error retrieving URL data:", e)
            return None       
    @staticmethod
    def get_requirement_doc(feature_id):
        try:
            with Session(engine) as session: stmt = ( 
                            select(RequirementDocument)
                            .join(Feature, RequirementDocument.id == Feature.requirement_document_id)
                            .where(Feature.id == feature_id)
                        )
            return session.exec(stmt).last()
        except:
            return None        