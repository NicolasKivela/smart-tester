import asyncio
import json
import os
from .page_navigator import PageNavigator # Import the refactored navigator
from .locator_agent import LocatorRetrievalAgent
from .navigator_agent import NavigatorAgent
from .task_agent import BDDTaskAgent
from .filter_agent import FilterAgent
from ..requirement_handling.storage import URL_DATA




async def main():
    
    URL="https://www.hsl.fi"
    
    credentials = URL_DATA.username + "," + URL_DATA.password
    all_found_locators = []
    action_history = []

    # Initialize agents
    navigator_agent = NavigatorAgent()
    locator_agent = LocatorRetrievalAgent()
    task_agent = BDDTaskAgent()
    filter_agent = FilterAgent()
    
    # Path to scenarios.json
    scenarios_json_path = os.path.join(os.path.dirname(__file__), 'json_files', 'scenarios.json')

    # Load scenarios from the JSON file
    scenarios = []
    try:
        with open(scenarios_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            scenarios = data.get("scenarios", []) # Assuming scenarios are under a "scenarios" key
    except FileNotFoundError:
        print(f"Error: scenarios.json not found at {scenarios_json_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {scenarios_json_path}")
        return

    if not scenarios:
        print("No scenarios found in scenarios.json. Exiting.")
        return

    scenarios_str = "\n".join(scenarios)
    task_prompt =  """ User checks real-time departures for a stop Given the user is on the HSL.fi homepage 
    When the user searches for stop Rautatientori 
    Then the system should display a list of upcoming departures
    And each departure should show line number, destination, and minutes until departure"""
    task = await task_agent.execute_task(task_prompt)
    test_task = """ 1. Go to https://www.hsl.fi
                2. Fill the "From" field with "Helsinki Central Railway Station"
                3. Click the "Helsinki Central Railway Station" suggestion
                4. Fill the "To" field with "Espoo"
                5. Click the "Espoo" suggestion
                6. finish
                """
  
    

    # Initialize the navigator
    video_path = os.path.join(os.path.dirname(__file__), 'videos')
    navigator = PageNavigator(video_path=video_path)

    try:
        await navigator.start()
        # Initial navigation and cookie handling
        #await navigator.goto(URL_DATA.url)
        await navigator.goto(URL)

        # Main loop
        for i in range(10): # Set a max of 10 iterations to prevent infinite loops

            #There seems to be cookies in every page. Accept them
            await navigator.accept_cookies()

            if not navigator.page:
                print("Page object is not available. Exiting.")
                break

            print(f"\n--- Iteration {i+1} ---")
            print(f"Current URL: {navigator.page.url}")
            
            # 1. Scrape page using the navigator
            locator_input = await navigator.get_page_content_for_agent(test_task)
            
            print("Asking LocatorAgent to find relevant locators...")
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
                        print(f"Found {len(newly_found_locators['locators'])} new locators.")
                else:
                    print("No JSON object found in LocatorAgent response.")
            except json.JSONDecodeError:
                print(f"Could not decode JSON from LocatorAgent response: {relevant_locators_json_str}")
            
            # 2. Filter duplicate locators
            if all_found_locators: # Only filter if there are locators
                filter_prompt = f'''
                This is the list of locators:
                {json.dumps(all_found_locators, indent=2)}
                '''
                print(f"Asking FilterAgent to process {len(all_found_locators)} locators...")
                filtered_locators_str = await filter_agent.execute_task(filter_prompt)
                
                try:
                    # The model might return a JSON object or a JSON array.
                    # Let's find the start and end of the JSON, whether it's { or [
                    start_char = '[' if '[' in filtered_locators_str else '{'
                    start_index = filtered_locators_str.find(start_char)
                    end_char = ']' if start_char == '[' else '}'
                    end_index = filtered_locators_str.rfind(end_char)

                    if start_index != -1 and end_index != -1:
                        json_part = filtered_locators_str[start_index : end_index + 1]
                        parsed_data = json.loads(json_part)
                        
                        if isinstance(parsed_data, list):
                            # If the agent returned a list directly, use it.
                            all_found_locators = parsed_data
                        elif isinstance(parsed_data, dict):
                            # If it returned a dictionary, try to find the list of locators within it.
                            found_list = False
                            for key, value in parsed_data.items():
                                if isinstance(value, list):
                                    all_found_locators = value
                                    found_list = True
                                    break
                            if not found_list:
                                print("FilterAgent returned a dictionary, but no list of locators was found inside it. Keeping original list.")
                        
                        print(f"FilterAgent finished. Unique locators: {len(all_found_locators)}")
                    else:
                        print("No JSON object or array found in FilterAgent response, keeping original list.")
                except json.JSONDecodeError:
                    print(f"Could not decode JSON from FilterAgent response: {filtered_locators_str}")
                    print("Continuing with unfiltered locators.")

            # 3. Decide next action with NavigatorAgent
            navigator_prompt = f'''
            Overall Task: {test_task}

            Action History (what has been done so far):
            {json.dumps(action_history, indent=2)}

            Locators found on the CURRENT page:
            {json.dumps(newly_found_locators, indent=2)}

            Username and password:
            {json.dumps(credentials, indent=2)}

            Based on the task, history, and current page locators, what is the single next action to perform?
            Provide a robust CSS or XPath selector.
            If the task is complete, respond with action 'finish'.
            Your response must be a single JSON object with a list of 'actions'.
            Example for click: {{"actions": [{{"action": "click", "css": "a[href='/tickets']", "description": "Navigate to tickets page."}}]}}
            Example for fill: {{"actions": [{{"action": "fill", "css": "input#username", "xpath": "//input[@id='username']", "possible text": "myuser", "description": "Fill the username field."}}]}}
            Example for finish: {{"actions": [{{"action": "finish", "reason": "The ticket price has been found."}}]}}
            '''
            
            print(f"Asking NavigatorAgent to decide the next action...")
            next_action_str = await navigator_agent.execute_task(navigator_prompt)

            # 4. Parse and execute the action
            try:
                start_index = next_action_str.find('{')
                end_index = next_action_str.rfind('}')
                if start_index == -1 or end_index == -1:
                    print(f"Error: Could not find a valid JSON object in NavigatorAgent response: {next_action_str}")
                    break
                json_part = next_action_str[start_index : end_index + 1]
                action_data = json.loads(json_part)
                action_list = action_data.get('actions', [])
                if not action_list:
                    print("NavigatorAgent returned no actions. Ending task.")
                    break
                action_details = action_list[0]
                action_history.append(action_details)

                if action_details.get("action") == "finish":
                    print(f"Task finished. Reason: {action_details.get('reason')}")
                    break

                # Use the navigator to execute the action
                await navigator.execute_action(action_details)

            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from NavigatorAgent response: {next_action_str}")
                break
            except Exception as e:
                print(f"An error occurred during action execution: {e}")
                break
    finally:
        # Final cleanup
        print("\n--- Task Execution Finished ---")
        print("\nFinal Action History:")
        print(json.dumps(action_history, indent=2))
        print(f"\nTotal Locators Found: {len(all_found_locators)}")
        print(json.dumps(all_found_locators, indent=2))
        if navigator:
            await navigator.stop()


if __name__ == "__main__":
    asyncio.run(main())