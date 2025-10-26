import asyncio
import json
from .page_navigator import PageNavigator # Import the refactored navigator
from .locator_agent import LocatorRetrievalAgent
from .navigator_agent import NavigatorAgent
from .task_agent import BDDTaskAgent

async def main():
    URL = "https://www.hsl.fi/"
    task = "First, navigate to the 'Responsibility' page. Then get locators related for opening the responsibility report from the responsibility page."

    all_found_locators = []
    action_history = []

    # Initialize agents
    navigator_agent = NavigatorAgent()
    locator_agent = LocatorRetrievalAgent()
    
    # Initialize the navigator
    navigator = PageNavigator()

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

            # 2. Decide next action with NavigatorAgent
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