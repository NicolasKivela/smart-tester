from .task_agent import BDDTaskAgent
from .locator_agent import LocatorRetrievalAgent
from .navigator_agent import NavigatorAgent
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json


async def main():

    URL = "https://www.hsl.fi/"

    all_relevant_locators = []

    input_for_task_agent =  "URL: https://www.hsl.fi/ Scenario: Browsing Different Ticket Types Given the user navigates to the Tickets and Prices section When the page loads Then the user should see distinct categories for different ticket types (e.g., Single Tickets, Day Tickets, Season Tickets) And clicking on a ticket type should provide a description of its validity and use. Scenario: Checking Prices by Travel Zone Given the user is viewing the pricing details for a specific ticket type (e.g., Season Ticket) When the user selects different travel zones (e.g., Zone AB, Zone BC, Zone D) Then the displayed price should update correctly for the selected zone combination And the user should be able to clearly identify the cost for their journey zone. Scenario: Finding Ticket Purchase Instructions Given the user is in the Tickets and Prices section When the user looks for information on where to buy tickets Then the page should list various purchase channels (e.g., HSL App, Ticket Machines, Service Points) And each channel should have clear, step-by-step instructions or links detailing the purchase process."

    task = "Get relevant locators from the Ticekts and prices page by navigating to the tickets and prices page"

    #Here starts the new script. Open the browser to the page.
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        # THis part could be wrapped to a scraping function
        await page.goto(URL, timeout=60000, wait_until="networkidle")

        html = await page.content()

        soup = BeautifulSoup(html, 'html.parser')

        selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit']
        elements = soup.find_all(selectors)

        # This line is fine from your original code
        interactive_elements = [str(el) for el in elements]
        # --- Fix ---
        # 1. Join the list of elements into a single, comma-separated string
        locators_string = ", ".join(interactive_elements)
        # 2. Use an f-string to format the output exactly as requested
        locator_input = f"Locators: {locators_string}, Task: {str(task)}"

        #Init agents 
        navigator_agent = NavigatorAgent()
        locator_agent = LocatorRetrievalAgent()

        # Get relevant locators from the scraped content using the agent
        relevant_locators = await locator_agent.execute_task(locator_input)
        print(f"Printing relevant locators for debugging purposes {relevant_locators} and appending them to the list")
        all_relevant_locators.append(relevant_locators)

        # Use navigator agent with the found locators and task to decide the next action
        navigator_input = f"Task: {task}, Relevant locators: {relevant_locators}"
        print(navigator_input)
        next_task = await navigator_agent.execute_task(navigator_input)
        print(f"Next task would be: {next_task}")

        # Parse the output to find the action and use playwright tools to execute that action
        # 1. Find the start of the JSON (the first '{')
        start_index = next_task.find('{')

        # 2. Find the end of the JSON (the last '}')
        end_index = next_task.rfind('}')

        # 3. Extract *only* the JSON part
        if start_index != -1 and end_index != -1:
            json_part = next_task[start_index : end_index + 1]
            
            # 4. Now, parse ONLY the extracted part
            try:
                data = json.loads(json_part)
                
                # --- Your original logic continues from here ---
                
                action_list = data.get('actions', [])
                
                if action_list:
                    action_details = action_list[0]
                    action_type = action_details.get('action')
                    css_locator = action_details.get('css')
                    xpath_locator = action_details.get('xpath')

                    if action_type == "click":
                        if not css_locator and not xpath_locator:
                            print("Action was 'click' but no 'css' or 'xpath' selector was provided.")
                        else:
                            try:
                                if css_locator:
                                    print(f"Action is 'click'. Trying CSS selector: {css_locator}")
                                    await page.locator(css_locator).first.click(timeout=5000)
                                    print("CSS click successful.")
                                else:
                                    raise ValueError("No CSS selector provided, trying XPath.")
                            
                            except Exception as e:
                                print(f"CSS click failed or was skipped. Reason: {e}")
                                if xpath_locator:
                                    print(f"Trying XPath fallback: {xpath_locator}")
                                    try:
                                        await page.locator(xpath_locator).first.click()
                                        print("XPath click successful.")
                                    except Exception as e2:
                                        print(f"XPath click also failed: {e2}")
                                        raise e2
                                else:
                                    print("CSS click failed and no XPath fallback was provided.")
                                    raise e
                    
                    else:
                        print(f"Action was '{action_type}', not 'click'. Skipping.")
                        
                else:
                    print("No actions found in the JSON.")

            except json.JSONDecodeError:
                print(f"Error: Could not decode the *extracted* JSON part.")
                print(f"Extracted part was: {json_part}")
        else:
            print("Error: Could not find '{' or '}' in the input string.")

# TODO: Make this to a loop
# TODO: Add memory so that agents could now which part of the task already done
# TODO: Add 'finish' to the actions, when it is decided that the task list is done
# TODO: Collect all locators in to one list during each iteration.

if __name__ == "__main__":
    # You'll need to have Playwright installed: pip install playwright
    # And install the browsers: playwright install
    asyncio.run(main())