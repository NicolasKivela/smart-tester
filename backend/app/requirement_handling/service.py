import time
from .agents import RequirementAgent
from .schemas import Credentials,UrlCredentials
from .storage import db_requirements 
import re

class RequirementsProcessor:
    agent = RequirementAgent()

    def __init__(self,url,credentials_input: UrlCredentials, text, req_file):
        self.credentials_input = credentials_input
        self.req_file = req_file
        self.text = text
        self.topics = []
        self.summaries = {}
        self.url = url
        self.credentials = Credentials(username=credentials_input.username,password=credentials_input.password)
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
        try:
            #Save url and credentials
            db_requirements.save_credentials_data_local(self.credentials)
            doc_id = db_requirements.save_requirement_document(self.req_file,self.text, self.url)
            await self.process_req_document()
            # Summaries
            await self.summarize()
            # Detailed requirements
            requirements = await self.get_requirements()
            db_requirements.create_processed_req(requirements, self.summaries, self.topics, doc_id,app_url=self.url)
            return {"status_code":200,"message":"Succesfully processed requirements"}
        except Exception as e:
            return {"status_code": 400, "Message":f"Error processing requirements: {e}"}