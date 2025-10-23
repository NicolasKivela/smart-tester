import asyncio
from navigator import navigate_site
from Task_agent import BDDTaskAgent, load_scenarios
import json

def main():
    url, scenarios = load_scenarios("scenarios.json")
    agent = BDDTaskAgent(model="gemini-2.5-flash")
    plan = agent.generate_task_plan(url, scenarios)
    print("\n🧭 Generated Task Plan:")
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    start_url = "https://www.hsl.fi"
    task = "Find locators relevant tockets and prices"
    depth = int(input("Kuinka syvälle mennään (esim. 2): "))
    asyncio.run(navigate_site(start_url, task, max_depth=depth))

if __name__ == "__main__":
    main()
