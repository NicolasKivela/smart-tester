import asyncio
import json
import os
from .page_navigator import PageNavigator # Import the refactored navigator
from .locator_agent import LocatorRetrievalAgent
from .navigator_agent import NavigatorAgent
from .task_agent import BDDTaskAgent

async def main():
    URL = "https://www.hsl.fi/"
    

    all_found_locators = []
    action_history = []

    # Initialize agents
    navigator_agent = NavigatorAgent()
    locator_agent = LocatorRetrievalAgent()
    task_agent = BDDTaskAgent()
    
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
    task_prompt = f"URL: {URL}\n\nBDD Scenarios:\n{scenarios_str}"
    task = await task_agent.execute_task(task_prompt)
    print(task)

    # Initialize the navigator
    video_path = os.path.join(os.path.dirname(__file__), 'videos')
    navigator = PageNavigator(video_path=video_path)

    try:
        await navigator.start()
        # Initial navigation and cookie handling
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
            locator_input = await navigator.get_page_content_for_agent(task)
            
            print("Asking LocatorAgent to find relevant locators...")
            relevant_locators_json_str = await locator_agent.execute_task(locator_input)
            
            newly_found_locators = {}
            try:
                # Extract JSON from markdown code block if present
                if '```json' in relevant_locators_json_str:
                    json_part = relevant_locators_json_str.split('```json\n', 1)[1].rsplit('\n```', 1)[0]
                else: # Fallback to original logic
                    start_index = relevant_locators_json_str.find('{')
                    end_index = relevant_locators_json_str.rfind('}')
                    if start_index != -1 and end_index != -1:
                        json_part = relevant_locators_json_str[start_index : end_index + 1]
                    else:
                        json_part = relevant_locators_json_str # Assume the whole string is JSON

                newly_found_locators = json.loads(json_part)
                if newly_found_locators.get("locators"):
                    all_found_locators.extend(newly_found_locators["locators"])
                    print(f"Found {len(newly_found_locators['locators'])} new locators.")
            except (json.JSONDecodeError, IndexError):
                print(f"Could not decode JSON from LocatorAgent response: {relevant_locators_json_str}")
                newly_found_locators = {} # Ensure it's a dict for the next step

            # 2. Decide next action with NavigatorAgent
            navigator_prompt = f'''
            Overall Task: {task}

            Action History (what has been done so far):
            {json.dumps(action_history, indent=2)}

            Locators found on the CURRENT page:
            {json.dumps(newly_found_locators, indent=2)}

            Based on the task, history, and current page locators, what is the single next action to perform?
            **You MUST use one of the locators provided in "Locators found on the CURRENT page" for your action.**
            Provide a robust CSS or XPath selector from the provided locators.
            If the task is complete, respond with action 'finish'.
            Your response must be a single JSON object with a list of 'actions'.
            Example for click: {{"actions": [{{"action": "click", "css": "a[href='/tickets']", "description": "Navigate to tickets page."}}]}}
            Example for fill: {{"actions": [{{"action": "fill", "css": "input#username", "xpath": "//input[@id='username']", "possible text": "myuser", "description": "Fill the username field."}}]}}
            Example for finish: {{"actions": [{{"action": "finish", "reason": "The ticket price has been found."}}]}}
            '''
            
            print(f"Asking NavigatorAgent to decide the next action...")
            next_action_str = await navigator_agent.execute_task(navigator_prompt)

            # 3. Parse and execute the action
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