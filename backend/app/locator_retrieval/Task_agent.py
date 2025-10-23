import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY puuttuu .env tiedostosta")

client = genai.Client(api_key=api_key)

task_agent_prompt = """ 
You are a web automation planning expert.

You receive one or more BDD scenarios and a URL. 
Your job is to plan a single efficient route through the website that satisfies ALL BDD scenarios 
with the minimum number of steps.

Each step must be valid JSON and contain:
- "action": open_page, click, input, verify_text, wait, etc.
- "target": a short natural-language description of the element to find
- "details": extra info such as input value or expected text

Output ONLY valid JSON in this format:
[
  {"action": "...", "target": "...", "details": "..."},
  ...
]
"""

class BDDTaskAgent:
    def __init__(self, model="gemini-2.5-flash", output_file="tasks.json"):
        self.model = model
        self.output_file = output_file

        # luodaan tiedosto jos ei ole
        if not os.path.exists(self.output_file):
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump({"tasks": []}, f, indent=2, ensure_ascii=False)

    def generate_task_plan(self, url: str, bdd_scenarios: list[str]) -> list[dict]:
        """Send BDD scenarios to Gemini and return structured JSON task plan"""
        scenarios_text = "\n".join(f"- {s}" for s in bdd_scenarios)
        full_prompt = f"{task_agent_prompt}\n\nWebsite: {url}\n\nBDD Scenarios:\n{scenarios_text}"

        print("🧠 Generating task plan with Gemini...")
        response = client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )

        text = response.text.strip()
        try:
            plan = json.loads(text)
        except json.JSONDecodeError:
            print("⚠️ Model response was not pure JSON, attempting to extract JSON block...")
            import re
            json_match = re.search(r"\[.*\]", text, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group(0))
            else:
                raise ValueError(f"❌ No valid JSON found in model response:\n{text}")

        # tallenna tiedostoon
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump({"tasks": plan}, f, indent=2, ensure_ascii=False)

        print(f"✅ Task plan saved to {self.output_file}")
        return plan


def load_scenarios(filepath="scenarios.json"):
    """Load BDD scenarios and URL from JSON file"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["url"], data["scenarios"]


if __name__ == "__main__":
    url, scenarios = load_scenarios("scenarios.json")

    agent = BDDTaskAgent(model="gemini-2.5-flash")
    plan = agent.generate_task_plan(url, scenarios)

    print("\n🧭 Generated Plan:")
    print(json.dumps(plan, indent=2, ensure_ascii=False))