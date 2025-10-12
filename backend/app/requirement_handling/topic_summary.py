from app.requirement_handling.llm_client import client

def summarize_topic(text, topic):
    """Summarize content related to a topic using LLM."""
    prompt = f"""
    You are an assistant analyzing software requirements.
    Summarize all information related to the topic "{topic}".
    Do not invent content, only summarize what exists.

    Text:
    {text[:12000]}
    """

    response = client.generate_content(prompt)
    return response.text.strip()