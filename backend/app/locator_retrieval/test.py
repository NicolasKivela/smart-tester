import asyncio
import json
import os
from app.locator_retrieval.page_navigator import PageNavigator 
from app.locator_retrieval.agents.locator_agent import LocatorRetrievalAgent
from app.locator_retrieval.agents.navigator_agent import NavigatorAgent
from app.locator_retrieval.agents.task_agent import BDDTaskAgent

async def main():
    URL = "https://www.hsl.fi/en"
    task = f"""1. Navigate to the tickets and fares.
               2. Choose student as the customer groupd in ABC zone
               3. Show prices
               4. See price for the single day ticket
               """

    all_found_locators = []
    action_history = []

    # Initialize agents
    navigator_agent = NavigatorAgent()
    locator_agent = LocatorRetrievalAgent()
    task_agent = BDDTaskAgent()
    
    # Initialize the navigator
    # Ensure video directory exists
    video_dir = os.path.join(os.path.dirname(__file__), "videos")
    os.makedirs(video_dir, exist_ok=True)
    
    navigator = PageNavigator(headless=True, silent=False)

    try:
        await navigator.start(record_video_dir=video_dir)
        # Initial navigation and cookie handling
        await navigator.goto(URL)

        # Main loop
        for i in range(10): # Set a max of 10 iterations to prevent infinite loops
   
            await navigator.iteration_screenshot(i)

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
            
            # Capture aria snapshot and screenshot
            aria_snapshot = await navigator.get_aria_snapshot()
            screenshot = await navigator.get_screenshot()

            # Construct prompt using NavigatorAgent's method
            navigator_prompt = navigator_agent.construct_prompt(
                task=task,
                history=action_history,
                locators=newly_found_locators,
                aria_snapshot=aria_snapshot,
                screenshot=screenshot
            )
            
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
            if navigator.page:
                try:
                    video = await navigator.page.video.path()
                    print(f"\nVideo saved to: {video}")
                except Exception as e:
                    print(f"Could not get video path: {e}")
            await navigator.stop()


if __name__ == "__main__":
    asyncio.run(main())