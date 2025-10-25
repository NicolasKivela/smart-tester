from .task_agent import BDDTaskAgent
from .locator_agent import LocatorRetrievalAgent
import asyncio


async def main():

    input =  "URL: https://www.hsl.fi/ Scenario: Browsing Different Ticket Types Given the user navigates to the Tickets and Prices section When the page loads Then the user should see distinct categories for different ticket types (e.g., Single Tickets, Day Tickets, Season Tickets) And clicking on a ticket type should provide a description of its validity and use. Scenario: Checking Prices by Travel Zone Given the user is viewing the pricing details for a specific ticket type (e.g., Season Ticket) When the user selects different travel zones (e.g., Zone AB, Zone BC, Zone D) Then the displayed price should update correctly for the selected zone combination And the user should be able to clearly identify the cost for their journey zone. Scenario: Finding Ticket Purchase Instructions Given the user is in the Tickets and Prices section When the user looks for information on where to buy tickets Then the page should list various purchase channels (e.g., HSL App, Ticket Machines, Service Points) And each channel should have clear, step-by-step instructions or links detailing the purchase process."

    agent1 = BDDTaskAgent()
 
    task = await agent1.execute_task(input)
    print("--TASK--")
    print(task)

    agent2 = LocatorRetrievalAgent()

    task = "Get relevant locators from the main page related to navigating to customer service, tickets and prices, traveling and login"
    print(f"Overwriting the task manually for now. Task: {task}")
    
    locators = await agent2.execute_task(f"My task is to test the BDD scenarios, and for that I need locators. This is the plan to follow: {task}. Please provide all locators from https://www.hsl.fi needed to follow the plan.")
    print("--LOCATORS--")
    print(locators)

if __name__ == "__main__":
    # You'll need to have Playwright installed: pip install playwright
    # And install the browsers: playwright install
    asyncio.run(main())