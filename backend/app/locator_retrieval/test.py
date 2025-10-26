import asyncio
import json
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

# These imports are based on the user's provided file.
# This script assumes these agent modules exist in the same directory.
from .locator_agent import LocatorRetrievalAgent
from .navigator_agent import NavigatorAgent

async def scrape_page_for_input(page: Page, task: str) -> str:
    """
    Scrapes the current page, extracts interactive elements, and formats them
    as input for the LocatorRetrievalAgent.
    """
    print("Scraping current page for interactive elements...")
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"Page did not reach network idle state, continuing anyway. Reason: {e}")

    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')

    selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit']
    elements = soup.find_all(selectors)
    
    interactive_elements = [str(el) for el in elements]
    locators_string = ", ".join(interactive_elements)
    
    # Format the string for the agent
    return f"URL: {page.url}, Locators: {locators_string}, Task: {str(task)}"

async def execute_action(page: Page, action_details: dict):
    """
    Executes a single action (e.g., 'click') provided by the NavigatorAgent.
    """
    action_type = action_details.get('action')
    description = action_details.get('description', 'No description')
    
    if action_type == "click":
        # The navigator agent should provide a single, robust selector.
        selector = action_details.get('css') or action_details.get('xpath')
        
        if not selector:
            print("Action was 'click' but no 'css' or 'xpath' selector was provided.")
            return

        try:
            print(f"Executing action: '{description}' by clicking selector: {selector}")
            await page.locator(selector).first.click(timeout=10000)
            print("Click successful.")
            # Wait for the page to settle after the click
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            print(f"Click action failed for selector '{selector}'. Reason: {e}")
            # Re-raise the exception to stop the loop on a critical failure
            raise e
    else:
        print(f"Action was '{action_type}', not 'click'. Skipping execution.")

async def main():
    URL = "https://www.hsl.fi/"
    task = "First, navigate to the 'Responsibility' page. Then get locators related for opening the responsibility report"

    all_found_locators = []
    action_history = []


    # Initialize agents
    navigator_agent = NavigatorAgent()
    locator_agent = LocatorRetrievalAgent()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        await page.goto(URL, timeout=60000, wait_until="networkidle")

        # Main loop to perform the navigation task
        for i in range(10): # Set a max of 10 iterations to prevent infinite loops
            print(f"\n--- Iteration {i+1} ---")
            print(f"Current URL: {page.url}") # Print current URL at the start of the iteration
            
            # 1. Scrape page to find locators relevant to the current sub-task
            locator_input = await scrape_page_for_input(page, task)

            #print(f"Interactive elements found: {locator_input}")
            
            print("Asking LocatorAgent to find relevant locators...")
            relevant_locators_json_str = await locator_agent.execute_task(locator_input)

            #print(f"relevant locators found from the current page: {relevant_locators_json_str}")
            
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

            # 2. Decide the next action using NavigatorAgent (which now has memory)
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
            
            print(f"Asking NavigatorAgent to decide the next action... with {navigator_prompt}")
            next_action_str = await navigator_agent.execute_task(navigator_prompt)

            # 3. Parse and execute the action from the NavigatorAgent
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

                await execute_action(page, action_details)

            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from NavigatorAgent response: {next_action_str}")
                break
            except Exception as e:
                print(f"An error occurred during action execution: {e}")
                break

        print("\n--- Task Execution Finished ---")



        print("\nFinal Action History:")
        print(json.dumps(action_history, indent=2))
        print(f"\nTotal Locators Found: {len(all_found_locators)}")
        print(json.dumps(all_found_locators, indent=2)) # Uncomment to see all locators

if __name__ == "__main__":
    asyncio.run(main())
