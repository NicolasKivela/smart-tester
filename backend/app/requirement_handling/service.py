import time
from .agents import RequirementAgent
from .save_file import save_to_file
from .schemas import Credentials
from app.common.models.req_model import Processed_Req, Extracted_Reqs
from .storage import REQUIREMENTS,db_requirements 
import re

class RequirementsProcessor:
    agent = RequirementAgent()

    def __init__(self, json_input, text, req_file):
        self.json_input = json_input
        self.req_file = req_file
        self.text = text
        self.topics = []
        self.summaries = {}
        self.url = json_input["url"]
        self.credentials = Credentials(password=json_input["password"], username=json_input["username"])
    async def process_req_document(self):
        """Ask the model for topics, then extract them cleanly."""
        topics_text = await self.agent.detect_topics(self.text)
        try:
            self.topics = topics_text
            return self.topics
        except Exception as e:
            print("Error saving topics temporary", e)
    
    async def summarize(self):
        for topic in self.topics:
            summary = await self.agent.summarize_topic(self.text,topic)
            self.summaries[topic] = summary
            time.sleep(5)
        return self.summaries
    
    async def get_requirements(self):
        results = {}
        for topic in self.topics:
            raw_reqs = await self.agent.extract_requirements(self.text, topic
            )
            # Convert string output into list of clean lines
            if isinstance(raw_reqs, str):
                req_list = [line.strip("-*• ") for line in raw_reqs.split("\n") if line.strip()]
            elif isinstance(raw_reqs, list):
                req_list = raw_reqs
            else:
                req_list = [str(raw_reqs)]

            results[topic] = req_list
        return results

    async def run_pipeline(self):
        #Save url and credentials
        #db_requirements.save_url_data(self.url, self.credentials)
        await self.process_req_document()
        # Summaries
        await self.summarize()
        # Detailed requirements
        requirements = await self.get_requirements()
        #db_requirements.create_processed_req(requirements, self.summaries, self.topics)
        reqs = await self.get_requirements()

        db_req = Processed_Req(
        feature=self.topics,
        summary=self.summaries,
        )
        extracted_reqs = []
        for req in requirements:
            extracted_reqs.append(Extracted_Reqs(topic_reqs=req))
        db_req.requirements = extracted_reqs
        return db_req
def get_requirements(req_id):
    return REQUIREMENTS[req_id]
