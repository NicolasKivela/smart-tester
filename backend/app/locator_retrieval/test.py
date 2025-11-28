import asyncio
import json
import os
from app.locator_retrieval.page_navigator import PageNavigator 
from app.locator_retrieval.agents.locator_agent import LocatorRetrievalAgent
from app.locator_retrieval.agents.navigator_agent import NavigatorAgent
from app.locator_retrieval.agents.task_agent import BDDTaskAgent

async def main():
    URL = "https://www.hsl.fi/en"
    task = f"""1. Verify you have a journey planner available
               2. Use 'Kamppi' as the starting address
               3. Use 'Helsinki train station' as the destination address
               4. Search the route from 'Kamppi' to 'Helsinki train station'
               6. Verify that route suggestions are visible
               """

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
    # Ensure video directory exists
    video_dir = os.path.join(os.path.dirname(__file__), "videos")
    os.makedirs(video_dir, exist_ok=True)
    
    navigator = PageNavigator(headless=True, silent=False)

    try:
        await navigator.start(record_video_dir=video_dir)
        # Initial navigation and cookie handling
        #await navigator.goto(URL_DATA.url)
        await navigator.goto(URL)

        current_task = task

        # Main loop
        for i in range(15): # Set a max of 15 iterations to prevent infinite loops
   
            await navigator.iteration_screenshot(i)

            if not navigator.page:
                print("Page object is not available. Exiting.")
                break

            print(f"\n--- Iteration {i+1} ---")
            print(f"Current URL: {navigator.page.url}")
            
            # Capture aria snapshot and screenshot. Used for locator agent and navigator agent to understand the page.
            aria_snapshot = await navigator.get_aria_snapshot()
            screenshot = await navigator.get_screenshot()

            scraped_elements = await navigator.get_page_content_for_agent(task)
            locator_input = locator_agent.construct_prompt(scraped_elements, aria_snapshot, screenshot)
            
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
                            page_url = locator.get("locator found from")
                            
                            # Check if valid (at least one selector is present and not N/A)
                            is_valid = (css and css != "N/A") or (xpath and xpath != "N/A")
                            
                            if is_valid:
                                # Check if duplicate (CSS/XPath AND URL must match)
                                is_duplicate = False
                                for existing in all_found_locators:
                                    existing_url = existing.get("locator found from")
                                    # If URLs are different, they are not duplicates even if selectors match
                                    if page_url != existing_url:
                                        continue
                                        
                                    if (css and css != "N/A" and existing.get("css") == css) or \
                                       (xpath and xpath != "N/A" and existing.get("xpath") == xpath):
                                        is_duplicate = True
                                        break
                                
                                if not is_duplicate:
                                    all_found_locators.append(locator)
                        
                        print(f"Found {len(newly_found_locators['locators'])} new locators (after filtering).")

                else:
                    print("No JSON object found in LocatorAgent response.")
            except json.JSONDecodeError:
                print(f"Could not decode JSON from LocatorAgent response: {relevant_locators_json_str}")

            # 2. Decide next action with NavigatorAgent

            # Construct prompt using NavigatorAgent's method
            navigator_prompt = navigator_agent.construct_prompt(
                task=current_task,
                history=action_history,
                locators=newly_found_locators,
                aria_snapshot=aria_snapshot,
                screenshot=screenshot
            )
            
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
                
                # Update task progress
                if action_data.get("updated_task"):
                    current_task = action_data["updated_task"]
                    print(f"Task updated:\n{current_task}")

                action_list = action_data.get('actions', [])
                if not action_list:
                    print("NavigatorAgent returned no actions. Ending task.")
                    break
                
                action_details = action_list[0]
                
                if action_details.get("action") == "finish":
                    print(f"Task finished. Reason: {action_details.get('reason')}")
                    action_history.append(action_details)
                    break

                # Use the navigator to execute the action
                try:
                    await navigator.execute_action(action_details)
                    action_details["status"] = "success"
                except Exception as e:
                    print(f"Action failed: {e}")
                    action_details["status"] = "failure"
                    action_details["error"] = str(e)
                
                action_history.append(action_details)

            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from NavigatorAgent response: {next_action_str}")
                break
            except Exception as e:
                print(f"An error occurred during action processing: {e}")
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