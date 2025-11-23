from app.common.base_agent import BaseAgent
from app.requirement_handling.schemas import Extracted_Reqs
import json, re

class RequirementAgent(BaseAgent):
    def __init__(self,  session_id: str):
        super().__init__(session_id=session_id, agent="requirement_agent")
        
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

    async def detect_topics(self, text: str):
        prompt = f"""
        You are an assistant that analyzes requirement documents.
        From the text below, identify all the main features as topics.
        Features are for example: Login, Checkout, Shopping Cart, Payment, etc.

        Return the result as a JSON list of topic names only.
        {{[
            feature_title1,
            feature_title2,
            etc.
        ]}}
        Requirement document to analyze: 
        {text}
        """

        content = await self.execute_task(prompt)
        print("Raw content from topics",content)
        try:
            return json.loads(content)
        except:
            return list(set(re.findall(r'"([^"]+)"', content)))
    

    async def extract_requirements(self, text: str, topic: str):
        prompt = f"""
        You are a requirement extraction assistant.
        From the document text below, extract all functional or testable requirements
        related to the topic "{topic}".
        Each requirement should be a single clear sentence.

        Return output as a JSON list
        {{
            "topic":[requirements here]
        }}

        Text:
        {text[:12000]}
        """
        content = await self.execute_task(prompt, response_format=Extracted_Reqs)
        try:
            json_content = json.loads(content)
            return json_content.get("topic_reqs")
        except Exception as e:
            print(e)
            return 
    

    async def summarize_topic(self, text: str, topic: str):
        prompt = f"""
        You are an assistant analyzing software requirements.
        Summarize all information related to the topic "{topic}".
        Do not invent content, only summarize what exists.

        Text:
        {text[:12000]}
        """
        return await self.execute_task(prompt)