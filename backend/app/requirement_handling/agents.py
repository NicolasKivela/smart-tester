from app.common.base_agent import BaseAgent
import json, re

class RequirementAgent(BaseAgent):
    def _get_system_message(self) -> str:
        return (
            "You are an intelligent assistant that analyzes software requirement documents. "
            "You detect topics, summarize them, and extract detailed requirements."
            "Always output clear, structured, and concise responses."
            "Do not translate the content."
        )

    def _get_tools(self):
        return None 

    def _get_tool_functions(self):
        return None

    # Custom Agent Methods

    def detect_topics(self, text: str):
        prompt = f"""
        You are an assistant that analyzes requirement documents.
        From the text below, identify all the main topics or sections.
        Topics can include features like Login, Checkout, Shopping Cart, Payment, etc.

        Return the result as a JSON list of topic names only.

        Text:
        {text[:8000]}
        """
        content = self.execute_task(prompt)
        try:
            return json.loads(content)
        except:
            return list(set(re.findall(r'"([^"]+)"', content)))
    

    def extract_requirements(self, text: str, topic: str):
        prompt = f"""
        You are a requirement extraction assistant.
        From the document text below, extract all functional or testable requirements
        related to the topic "{topic}".
        Each requirement should be a single clear sentence.

        Return output as a JSON list.

        Text:
        {text[:12000]}
        """
        return self.execute_task(prompt)
    

    def summarize_topic(self, text: str, topic: str):
        prompt = f"""
        You are an assistant analyzing software requirements.
        Summarize all information related to the topic "{topic}".
        Do not invent content, only summarize what exists.

        Text:
        {text[:12000]}
        """
        return self.execute_task(prompt)