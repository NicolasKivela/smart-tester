import asyncio
from app.bdd_scenarios.bdd_generation_agent import BddGenerationAgent
from app.bdd_scenarios.schemas import Generate_BDD, BDD_Scenario
from app.bdd_scenarios.storage import BDD_SCENARIOS

def parse_gherkin(gherkin_text: str, feature: str) -> list[BDD_Scenario]:
    """
    Parses Gherkin text and converts it into a list of BDD_Scenario objects.
    """
    scenarios = []
    # Split the text by "Scenario:" to separate individual scenarios
    scenario_blocks = [s.strip() for s in gherkin_text.split("Scenario:") if s.strip()]

    for i, block in enumerate(scenario_blocks):
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue

        scenario_title = lines[0]
        given, when, then = [], [], []
        current_section = None

        for line in lines[1:]:
            if line.startswith("Given"):
                current_section = given
                given.append(line.replace("Given ", "").strip())
            elif line.startswith("When"):
                current_section = when
                when.append(line.replace("When ", "").strip())
            elif line.startswith("Then"):
                current_section = then
                then.append(line.replace("Then ", "").strip())
            elif line.startswith("And") and current_section is not None:
                current_section.append(line.replace("And ", "").strip())

        new_id = len(BDD_SCENARIOS) + len(scenarios) + 1
        scenarios.append(
            BDD_Scenario(
                id=new_id,
                feature=feature,
                scenario=scenario_title,
                given=given,
                when=when,
                then=then
            )
        )
    return scenarios

async def generate_bdd_scenarios_logic(item: Generate_BDD) -> list[BDD_Scenario]:
    """
    Uses BddGenerationAgent to generate BDD scenarios and returns them as a list of BDD_Scenario objects.
    """
    agent = BddGenerationAgent()
    
    # Construct the user message for the agent
    user_message = f"Feature: {item.feature}\nRequirements:\n{item.prompt}"
    
    # Run the agent asynchronously
    generated_text = await asyncio.to_thread(agent.execute_task, user_message)
    
    # Parse the generated Gherkin text
    generated_scenarios = parse_gherkin(generated_text, item.feature)
    
    return generated_scenarios