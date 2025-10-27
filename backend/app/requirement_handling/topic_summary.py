from app.requirement_handling.agents import RequirementAgent

def summarize_topic(text, topic):
    agent = RequirementAgent()
    return agent.summarize_topic(text, topic)