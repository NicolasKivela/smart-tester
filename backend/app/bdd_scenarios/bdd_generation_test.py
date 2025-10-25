from .bdd_generation_agent import BddGenerationAgent
import asyncio

async def main():


    print("Initializing BDD Agent")
    agent = BddGenerationAgent()

    # The user prompt. The agent should understand it needs to use its tool.
    user_prompt_checkout_payment = """Create BDD scenarios for these requirements regarding Checkout and Payment feature:
    Guest checkout should be supported.
    Cart totals should update automatically when quantities change.
    If a promo code is applied, it should immediately update the total cost.
    Checkout should be a multi-step process including address, shipping method, payment, and confirmation.
    Guest checkout should prompt users for an email to send the receipt.
    The platform must integrate with Stripe for payments.
    The platform must integrate with PayPal for payments.
    All payment processing must be secure.
    All payment processing must be compliant with PCI DSS standards.
    The system must validate credit card info before submission.
    After successful payment, users should receive a confirmation email with an order summary.
    If payment fails, the order should not be created.
    Payment error messages should be clear and actionable.
    After checkout, an order should be created in the system with a unique ID.
    Customers should be able to track their order from their profile.
    All payment-related pages must use HTTPS.
    Sensitive data, including credit cards, should be encrypted in transit.
    Sensitive data, including credit cards, should never be logged.
    Transactional emails, including order confirmation, should be sent using SendGrid.
    All transactional emails should include company branding.
    All transactional emails should include links to order tracking."""

    feature_1_requirements_for_hsl = """Create BDD scenarios for these requirements regarding the Route Planner feature for HSL.fi web page:
    As a user, I want to search for a route by entering a start and end address, so that I can find the best connection to my destination.
    As a user, I want to use my current location as the starting point of the route with one click, so that I can quickly plan a trip while on the move.
    As a user, I want to see several different route options, so that I can choose the most suitable one for me based on travel time, means of transport, and walking distance. 
    As a user, I want to see the details of the selected route, such as stops, schedules, travel times, and possible transfers, so that I know exactly how the journey will proceed.
    """

    print(f"User Prompt: \"{feature_1_requirements_for_hsl}\"")
    print("-" * 20)

    final_response = await agent.execute_task(feature_1_requirements_for_hsl)

    print("\n--- BDD Agent's Final Response ---")
    print(final_response)
    print("-" * 28)

if __name__ == "__main__":
    asyncio.run(main())