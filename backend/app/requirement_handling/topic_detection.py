import json
import re
from app.requirement_handling.llm_client import client

def detect_topics(text):
    """Use LLM to detect main topics in the document."""
    prompt = f"""
    You are an assistant that analyzes requirement documents.
    From the text below, identify all the main topics or sections.
    Topics can include features like Login, Checkout, Shopping Cart, Payment, etc.

    Return the result as a JSON list of topic names only.

    Text:
    {text[:8000]}
    """


    response = client.generate_content(prompt)
    content = response.text.strip()
    try:
        topics = json.loads(content)
    except:
        topics = re.findall(r'"([^"]+)"', content)
    return list(set(topics))