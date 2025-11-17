import asyncio
import json
from .locator_retrieving import LocatorRetrieving

async def main():
    # --- Inputs for the service ---
    # You can change these values to test with different inputs.
    
    # The URL of the website to test
    url = "https://www.hsl.fi"

    # The BDD scenarios to guide the locator retrieval process
    scenarios = [
        "Scenario: Browsing Different Ticket Types\nGiven the user navigates to the Tickets and Prices section\nWhen the page loads\nThen the user should see distinct categories for different ticket types (e.g., Single Tickets, Day Tickets, Season Tickets)\nAnd clicking on a ticket type should provide a description of its validity and use.",
        "Scenario: Checking Prices by Travel Zone\nGiven the user is viewing the pricing details for a specific ticket type (e.g., Season Ticket)\nWhen the user selects different travel zones (e.g., Zone AB, Zone BC, Zone D)\nThen the displayed price should update correctly for the selected zone combination\nAnd the user should be able to clearly identify the cost for their journey zone.",
        "Scenario: Finding Ticket Purchase Instructions\nGiven the user is in the Tickets and Prices section\nWhen the user looks for information on where to buy tickets\nThen the page should list various purchase channels (e.g., HSL App, Ticket Machines, Service Points)\nAnd each channel should have clear, step-by-step instructions or links detailing the purchase process."
    ]

    # User credentials (optional, not used in the current implementation)
    user_credentials = None

    # ---------------------------------

    # Instantiate the class
    locator_retriever = LocatorRetrieving()

    # Call the service
    print(f"--- Starting locator retrieval service for {url} ---")
    found_locators = await locator_retriever.locator_retrieving_service(
        scenarios=scenarios,
        url=url,
        user_credentials=user_credentials
    )

    # Print the output
    print("\n--- Locator Retrieval Service Finished ---")
    print(f"Total Locators Found: {len(found_locators)}")
    print("\n--- Found Locators ---")
    print(json.dumps(found_locators, indent=2))

if __name__ == "__main__":
    # This allows the async main function to be run.
    asyncio.run(main())
