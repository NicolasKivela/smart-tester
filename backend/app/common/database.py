from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///app/database.db"  

engine = create_engine(DATABASE_URL, echo=True)  

def init_db():
    from app.common.models.req_model import Feature, RequirementDocument,Requirement
    from app.common.models.bdd_model import BDDScenario
    from app.common.models.locator_model import LocatorElements
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
