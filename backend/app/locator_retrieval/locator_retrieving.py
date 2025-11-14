import asyncio
import json
from .page_navigator import PageNavigator
from app.locator_retrieval.agents import BDDTaskAgent,LocatorRetrievalAgent,NavigatorAgent
from app.requirement_handling.storage import REQUIREMENTS, URL_DATA, db_requirements
from app.bdd_scenarios.storage import db_bdd_scenarios
from app.requirement_handling.schemas import UrlCredentials
from app.locator_retrieval.storage import LOCATORS,db_locator

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
        self.task = task
        all_found_locators = []
        action_history = []

        navigator_agent = NavigatorAgent()
        locator_agent = LocatorRetrievalAgent()
        
        navigator = PageNavigator(headless=True, silent=True)

        try:
            await navigator.start()
            await navigator.goto(url)

            for _ in range(10): # Max 10 iterations
                # DEBUG PRINT
                print("still going")
                await navigator.accept_cookies()

                if not navigator.page:
                    break

                locator_input = await navigator.get_page_content_for_agent(task)
                
                relevant_locators_json_str = await locator_agent.execute_task(locator_input)
                
                newly_found_locators = {}
                try:
                    start_index = relevant_locators_json_str.find('{')
                    end_index = relevant_locators_json_str.rfind('}')
                    if start_index != -1 and end_index != -1:
                        json_part = relevant_locators_json_str[start_index : end_index + 1]
                        newly_found_locators = json.loads(json_part)
                        if newly_found_locators.get("locators"):
                            all_found_locators.extend(newly_found_locators["locators"])
                            for locator in newly_found_locators["locators"]:
                                description = locator["description"]
                                css = locator["css"]
                                xpath = locator["xpath"]
                                page_url = locator["locator found from"]
                                resp= db_locator.save_locator_item(locator_element_id,description=description,page_url=page_url, task=task, css=css, xpath=xpath)
                                print(resp)
                            print(newly_found_locators)
                except json.JSONDecodeError:
                    pass

                navigator_prompt = f'''
                Overall Task: {task}

                Action History (what has been done so far):
                {json.dumps(action_history, indent=2)}

                Locators found on the CURRENT page:
                {json.dumps(newly_found_locators, indent=2)}

                Based on the task, history, and current page locators, what is the single next action to perform?
                Provide a robust CSS or XPath selector.
                If the task is complete, respond with action 'finish'.
                Your response must be a single JSON object with a list of 'actions'.
                Example for click: {{"actions": [{{"action": "click", "css": "a[href='/tickets']", "description": "Navigate to tickets page."}}]}}
                Example for finish: {{"actions": [{{"action": "finish", "reason": "The ticket price has been found."}}]}}
                '''
                
                next_action_str = await navigator_agent.execute_task(navigator_prompt)

                try:
                    start_index = next_action_str.find('{')
                    end_index = next_action_str.rfind('}')
                    if start_index == -1 or end_index == -1:
                        break
                    json_part = next_action_str[start_index : end_index + 1]
                    action_data = json.loads(json_part)
                    action_list = action_data.get('actions', [])
                    if not action_list:
                        break
                    action_details = action_list[0]
                    action_history.append(action_details)

                    if action_details.get("action") == "finish":
                        break

                    await navigator.execute_action(action_details)

                except (json.JSONDecodeError, IndexError):
                    break
                except Exception:
                    break
        finally:
            if navigator:
                await navigator.stop()
        LOCATORS.append(all_found_locators)
        resp = db_locator.update_locator_element_status(locator_element_id)
        return LOCATORS
