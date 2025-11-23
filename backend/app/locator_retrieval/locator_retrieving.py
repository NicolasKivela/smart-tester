import asyncio
import json
from .page_navigator import PageNavigator
from app.locator_retrieval.agents import BDDTaskAgent,LocatorRetrievalAgent,NavigatorAgent
from app.requirement_handling.storage import REQUIREMENTS, URL_DATA, db_requirements
from app.bdd_scenarios.storage import db_bdd_scenarios
from app.requirement_handling.schemas import UrlCredentials
from app.common.models.locator_model import Status
from app.locator_retrieval.storage import LOCATORS,db_locator
from app.common.agent_config import AgentConfig
import os

class LocatorRetrieving:
    """
    A class to retrieve web element locators based on BDD scenarios.
    """
    def __init__(self, feature_id):
        self.feature_id = feature_id
        self.task = ""
    async def scraper_process(self):
        try:
            url_data = URL_DATA
            scenarios = db_bdd_scenarios.get_all_bdd_scenarios_by_feature(self.feature_id)
            print(scenarios)
            locators = asyncio.create_task(self.locator_retrieving_service(scenarios,url_data))
            #locators = self.locator_retrieving_service(scenarios,url_data)
            return {"status_code":200,"message":f"Locator process started,{locators}"}
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)=}")
            return {"status_code":400,"message":f"Error starting scraper process: {e.args}"}


    async def locator_retrieving_service(self, scenarios: list[dict], url_data: UrlCredentials):
        """
        Retrieves locators for web elements based on BDD scenarios by navigating a web page.

        Args:
            scenarios (list[str]): A list of BDD scenarios.
            url (str): The starting URL.
            user_credentials (dict, optional): User credentials for login. Defaults to None.

        Returns:
            list: A list of dictionaries, where each dictionary represents a found locator.
        """
        url = str(url_data.url)
        print(url)
        print(type(url))
        task_agent = BDDTaskAgent()
        scenarios_str = scenarios
        response = db_locator.save_locator_element(feature_id=self.feature_id,app_url=url,scenarios=scenarios)
        if response["status_code"] == 400:
            return response
        print(response)
        locator_element_id = response["body"]
        #scenarios_str = "\n".join(scenarios)
        task_prompt = f"URL: {url}\n\nBDD Scenarios:\n{scenarios_str}"
        task = await task_agent.execute_task(task_prompt)
        
        # DEBUG, remove later
        print(task)

        self.task = task
        current_task = task
        all_found_locators = []
        action_history = []

        navigator_agent = NavigatorAgent()
        locator_agent = LocatorRetrievalAgent()
        
        navigator = PageNavigator(headless=True, silent=True)

        try:
            record_video_dir = None
            if getattr(AgentConfig.NavigatorAgent, 'record_video', False):
                record_video_dir = os.path.join(os.path.dirname(__file__), "videos")
                os.makedirs(record_video_dir, exist_ok=True)
                
            await navigator.start(record_video_dir=record_video_dir)
            await navigator.goto(url)

            for i in range(15): # Max 15 iterations
                # DEBUG PRINT
                print("still going")
                # Remove this at some point
                if i == 0:
                    await navigator.accept_cookies()
                
                #Replace only with this method to get screenshots of each iteration
                await navigator.iteration_screenshot(i)

                if not navigator.page:
                    #Update locator element status
                    db_locator.update_locator_element_status(locator_element_id, Status.FAILURE)
                    break

                locator_input = await navigator.get_page_content_for_agent(scenarios_str)
                
                relevant_locators_json_str = await locator_agent.execute_task(locator_input)
                
                newly_found_locators = {}
                try:
                    start_index = relevant_locators_json_str.find('{')
                    end_index = relevant_locators_json_str.rfind('}')
                    if start_index != -1 and end_index != -1:
                        json_part = relevant_locators_json_str[start_index : end_index + 1]
                        newly_found_locators = json.loads(json_part)
                        if newly_found_locators.get("locators"):
                            for locator in newly_found_locators["locators"]:
                                css = locator.get("css")
                                xpath = locator.get("xpath")
                                
                                # Check if valid (at least one selector is present and not N/A)
                                is_valid = (css and css != "N/A") or (xpath and xpath != "N/A")
                                
                                if is_valid:
                                    # Check if duplicate (CSS/XPath AND URL must match)
                                    is_duplicate = False
                                    for existing in all_found_locators:
                                        existing_url = existing.get("locator found from")
                                        page_url = locator.get("locator found from")
                                        
                                        # If URLs are different, they are not duplicates even if selectors match
                                        if page_url != existing_url:
                                            continue

                                        if (css and css != "N/A" and existing.get("css") == css) or \
                                           (xpath and xpath != "N/A" and existing.get("xpath") == xpath):
                                            is_duplicate = True
                                            break
                                    
                                    if not is_duplicate:
                                        all_found_locators.append(locator)
                                        description = locator.get("description")
                                        page_url = locator.get("locator found from")
                                        resp= db_locator.save_locator_item(locator_element_id,description=description,page_url=page_url, task=task, css=css, xpath=xpath)
                                        print(resp)
                            print(f"Processed {len(newly_found_locators['locators'])} locators (filtered).")
                except json.JSONDecodeError:
                    pass

                # Capture aria snapshot and screenshot
                aria_snapshot = await navigator.get_aria_snapshot()
                screenshot = await navigator.get_screenshot()

                # Construct prompt using NavigatorAgent's method
                navigator_prompt = navigator_agent.construct_prompt(
                    task=current_task,
                    history=action_history,
                    locators=newly_found_locators,
                    aria_snapshot=aria_snapshot,
                    screenshot=screenshot
                )
                
                next_action_str = await navigator_agent.execute_task(navigator_prompt)

                try:
                    start_index = next_action_str.find('{')
                    end_index = next_action_str.rfind('}')
                    if start_index == -1 or end_index == -1:
                        #Update locator element status
                        db_locator.update_locator_element_status(locator_element_id, Status.FAILURE)
                        break
                    json_part = next_action_str[start_index : end_index + 1]
                    action_data = json.loads(json_part)
                    
                    # Update task progress
                    if action_data.get("updated_task"):
                        current_task = action_data["updated_task"]
                        print(f"Task updated:\n{current_task}")

                    action_list = action_data.get('actions', [])
                    if not action_list:

                        #Update locator element status
                        db_locator.update_locator_element_status(locator_element_id, Status.FAILURE)
                        break
                    action_details = action_list[0]

                    if action_details.get("action") == "finish":
                        #Update locator element status
                        db_locator.update_locator_element_status(locator_element_id, Status.READY)
                        action_history.append(action_details)
                        break

                    try:
                        await navigator.execute_action(action_details)
                        action_details["status"] = "success"
                    except Exception as e:
                        print(f"Action failed: {e}")
                        action_details["status"] = "failure"
                        action_details["error"] = str(e)
                    
                    action_history.append(action_details)

                except (json.JSONDecodeError, IndexError):
                        #Update locator element status
                    db_locator.update_locator_element_status(locator_element_id, Status.FAILURE)
                    break
                except Exception:
                        #Update locator element status
                    db_locator.update_locator_element_status(locator_element_id, Status.FAILURE)
                    break
        finally:
            if navigator:
                await navigator.stop()
        LOCATORS.append(all_found_locators)
        return LOCATORS
