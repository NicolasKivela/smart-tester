from app.requirement_handling.agents import RequirementAgent

def extract_requirements(text, topic):
    agent = RequirementAgent()
    return agent.extract_requirements(text, topic)