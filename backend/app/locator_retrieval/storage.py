import logging
from sqlmodel import Session, select
from typing import List,Dict,Any
from app.common.database import engine
from app.common.models import LocatorElements,BDDScenario
from app.common.models.locator_model import LocatorItem,LocatorSelector,Status
LOCATORS = {}
class db_locator():
    def save_locator_element(feature_id, app_url,scenarios):
        try:
            with Session(engine) as session:

                statement=(
                    select(BDDScenario)
                    .where(BDDScenario.feature_id ==feature_id)
                )
                scenarios = session.exec(statement).all()
                new_locator_element = LocatorElements(feature_id=feature_id, app_url=app_url,status=Status.ONGOING)
                new_locator_element.bdd_scenarios = scenarios
                session.add(new_locator_element)
                session.flush()
                locator_element_id = new_locator_element.id
                session.commit()
            return {"status_code":200, "message": "Locator element saved succesfully","body": locator_element_id}
        except Exception as e:
            print(e)
            return {"status_code":400, "message": "Error when saving locator element"}
    def update_locator_element_status(locator_element_id,status):
        try:
            with Session(engine) as session:
                locator_element = session.get(LocatorElements,locator_element_id)
                if locator_element is None:
                    return {
                        "status_code": 404,
                        "message": f"LocatorElement with id {locator_element_id} not found",
                    }
                locator_element.status = status
                session.commit()
                return {"status_code":200, "message":"status succesfully updated"}
        except Exception as e:
            return {"status_code":400, "message":f"Error occured when updating status: {e}"}
        
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
    def get_all_locator_data_by_feature_id(feature_id):
        try:
            with Session(engine) as session:
                statement = (
                    select(LocatorElements, LocatorItem, LocatorSelector)
                    .join(LocatorItem, LocatorItem.locator_id== LocatorElements.id)
                    .join(LocatorSelector, LocatorSelector.locator_item_id == LocatorItem.id)
                    .where(LocatorElements.feature_id == feature_id)
                )

                locator_element = session.exec(statement).all()
            body: List[Dict[str, Any]] = []
            for element, item, selector in locator_element:
                body.append({
                    "locator_element": element.model_dump() if hasattr(element, "model_dump") else element.dict(),
                    "locator_item": item.model_dump() if hasattr(item, "model_dump") else item.dict(),
                    "locator_selector": selector.model_dump() if hasattr(selector, "model_dump") else selector.dict(),
                })
            return {"status_code":200, "message": "Locator element fetched succesfully", "body": body}
        except:
            return {"status_code":400, "message": "Error when fetching locator element"}
    def save_locator_item(locator_element_id,description,page_url,task,css,xpath):
        try:
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
                selectors = session.exec(stmt).all()
                output = []
                for s in selectors:
                    s_output = {
                    "css": s.css,
                    "xpath": s.xpath,
                    "description": s.locator_item.description,
                    "page_url": s.locator_item.page_url,
                    }
                    output.append(s_output)
                return output
        except Exception as e:
            return {"status_code":400, "message": "Error fetching locator selectors"}



