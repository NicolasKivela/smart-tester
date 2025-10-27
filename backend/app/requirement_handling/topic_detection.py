from app.requirement_handling.agents import RequirementAgent

def detect_topics(text):
    agent = RequirementAgent()
    return agent.detect_topics(text)