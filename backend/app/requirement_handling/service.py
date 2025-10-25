from .storage import REQUIREMENTS
from .agents import RequirementAgent
from .save_file import save_to_file
from .schemas import Processed_Req
from .storage import REQUIREMENTS
import re

class RequirementsProcessor:
    agent = RequirementAgent()

    def __init__(self, json_input, text, req_file):
        self.json_input = json_input
        self.req_file = req_file
        self.text = text
        self.topics = []
        self.summaries = {}

    def process_req_document(self):
        """Ask the model for topics, then extract them cleanly."""
        topics_text = self.agent.execute_task(f"Detect topics in the document:\n{self.text}")

        # Try to extract lines that look like numbered topics
        matches = re.findall(r"\*\*(.*?)\*\*", topics_text)
        if matches:
            self.topics = [t.strip() for t in matches]
        else:
            # fallback: one topic
            self.topics = [topics_text.strip()]
        return self.topics
    
    def summarize(self):
        for topic in self.topics:
            summary = self.agent.execute_task(f"Summarize the document for topic '{topic}':\n{self.text}")
            self.summaries[topic] = summary
        return self.summaries
    
    def get_requirements(self):
        results = {}
        for topic in self.topics:
            raw_reqs = self.agent.execute_task(
                f"Extract detailed requirements for topic '{topic}':\n{self.text}"
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

    def run_pipeline(self):
        self.process_req_document()
        # Summaries
        self.summarize()
        # Detailed requirements
        requirements = self.get_requirements()

        # Combine all data into Processed_Req objects
        for i, topic in enumerate(self.topics, start=1):
            processed = Processed_Req(
                id=i,
                feature=topic,
                summary=re.sub(r'^\*\*Topic:.*?\*\*\s*', '', self.summaries.get(topic, ""), flags=re.MULTILINE),
                requirements=requirements.get(topic, []),
            )
            REQUIREMENTS[i] = processed.model_dump()



        reqs = self.get_requirements()
def get_requirements(req_id):
    return REQUIREMENTS[req_id]
