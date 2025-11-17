import logging
from sqlmodel import Session, select
from app.common.database import engine
from app.common.models import LocatorElements,BDDScenario
from app.common.models.locator_model import LocatorItem,LocatorSelector
LOCATORS = {}
#TODO: Add locator database CRUD logic here

class db_locator():
    def save_locator_element(feature_id, app_url,scenarios):
        try:
            with Session(engine) as session:

                statement=(
                    select(BDDScenario)
                    .where(BDDScenario.feature_id ==feature_id)
                )
                scenarios = session.exec(statement).all()
                new_locator_element = LocatorElements(feature_id=feature_id, app_url=app_url)
                print(new_locator_element)
                print(scenarios)
                new_locator_element.bdd_scenarios = scenarios
                session.add(new_locator_element)
                session.flush()
                locator_element_id = new_locator_element.id
                session.commit()
            print("body",new_locator_element)
            return {"status_code":200, "message": "Locator element saved succesfully","body": locator_element_id}
        except Exception as e:
            print(e)
            return {"status_code":400, "message": "Error when saving locator element"}

    def get_locator_element_by_id(locator_element_id):
        try:
            with Session(engine) as session:
                statement = (
                    select(LocatorElements)
                    .where(LocatorElements.id == locator_element_id)
                )

                locator_element = session.exec(statement).first()
            return {"status_code":200, "message": "Locator element fetched succesfully", "body": locator_element}
        except:
            return {"status_code":400, "message": "Error when fetching locator element"}
            
    def get_locator_element_by_feature_id(feature_id):
        try:
            with Session(engine) as session:
                statement = (
                    select(LocatorElements)
                    .where(LocatorElements.feature_id == feature_id)
                )

                locator_element = session.exec(statement).first()
            return {"status_code":200, "message": "Locator element fetched succesfully", "body": locator_element}
        except:
            return {"status_code":400, "message": "Error when fetching locator element"}
    
    def save_locator_item(locator_element_id,description,page_url,task,css,xpath):
        try:
            print("locator element id",locator_element_id)
            with Session(engine) as session:
                new_locator_item = LocatorItem(locator_id=locator_element_id,description=description,page_url=page_url,task=task)
                session.add(new_locator_item)
                session.flush()

                new_locator_selector = LocatorSelector(locator_item_id=new_locator_item.id,css=css,xpath=xpath)
                session.add(new_locator_selector)
                session.commit()
                session.refresh(new_locator_item)
                new_locator_selector = session.exec(
                select(LocatorSelector).where(LocatorSelector.locator_item_id == new_locator_item.id)
            ).all()
            return {"status_code": 200, "message": "Succesfully saved locator_item", "body": new_locator_selector}
        except Exception as e:
            return e

    def get_selectors_by_feature(feature_id: int):
        try:
            with Session(engine) as session:
                stmt = (
                    select(LocatorSelector)
                    .join(LocatorSelector.locator_item)        
                    .join(LocatorItem.locator)                     
                    .where(LocatorElements.feature_id == feature_id)
                )
                return session.exec(stmt).all()
        except Exception as e:
            return {"status_code":400, "message": "Error fetching locator selectors"}



