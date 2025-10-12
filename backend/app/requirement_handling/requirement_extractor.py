from app.requirement_handling.llm_client import client

def extract_requirements(text, topic):
    """Extract structured requirement sentences per topic."""
    prompt = f"""
    You are a requirement extraction assistant.
    From the document text below, extract all functional or testable requirements
    related to the topic "{topic}".
    Each requirement should be a single clear sentence.
    
    Return output as a JSON list.

    Text:
    {text[:12000]}
    """

    response = client.generate_content(prompt)
    return response.text.strip()