
import asyncio
import json
from .task_agent import BDDTaskAgent

async def main():
    # Load scenarios from the JSON file
    with open('app/locator_retrieval/json_files/scenarios.json', 'r') as f:
        scenarios_data = json.load(f)

    url = scenarios_data["url"]
    scenarios = scenarios_data["scenarios"]

    # Initialize the BDDTaskAgent
    task_agent = BDDTaskAgent()

    # Create the prompt for the agent
    scenarios_str = "\n".join(scenarios)
    task_prompt = f"URL: {url}\n\nBDD Scenarios:\n{scenarios_str}"

    # Execute the task and get the plan
    print("Asking BDDTaskAgent to create a plan...")
    plan = await task_agent.execute_task(task_prompt)

    # Print the generated plan
    print("\n--- Generated Plan ---")
    print(plan)

if __name__ == "__main__":
    asyncio.run(main())