import asyncio
from app.bdd_scenarios.bdd_generation_agent import BddGenerationAgent
from app.common.models.bdd_model import BDDScenario
from app.bdd_scenarios.schemas import BDD_Scenario
from app.bdd_scenarios.storage import BDD_SCENARIOS, db_bdd_scenarios
from app.requirement_handling.storage import db_requirements

def parse_gherkin(gherkin_text: str, feature: str, item_id) -> list[BDDScenario]:
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
        response = db_bdd_scenarios.add_bdd_scenarios(item_id,BDD_Scenario(
            scenario=scenario_title,
            content=block
        ))
        if response["status_code"] != 200:
            return response
    return response

async def generate_bdd_scenarios_logic(item_id: int) -> list[BDDScenario]:
    """
    Uses BddGenerationAgent to generate BDD scenarios and returns them as a list of BDD_Scenario objects.
    """
    feature_data = db_requirements.get_feature_data_by_id(item_id)

    session_id = "full_session"
    agent = BddGenerationAgent(session_id=session_id)
    
    # Construct the user message for the agent
    user_message = f"Feature: {feature_data.name}\nRequirements:\n{feature_data.requirements}"

    # Run the agent asynchronously
    generated_text = await agent.execute_task(user_message)
    # Parse the generated Gherkin text
    response = parse_gherkin(generated_text, feature_data, item_id)

    return response
