from .agents import RequirementAgent
from .save_file import save_to_file
class RequirementsProcessor:
    agent = RequirementAgent()
    def __init__(self, json_input, text, req_file):
        self.json_input = json_input
        self.req_file = req_file
        self.text = text
        self.topics = []
        self.summaries = {}
    def process_req_document(self):
        topics = self.agent.execute_task(f"Detect topics in the document:\n{self.text}")
        self.topics = topics if isinstance(topics, list) else [topics]
        return self.topics
    def save_input(self):
        with open("temp_input.txt", "wb") as f:
            f.write(self.text)
    def summarize(self):
        for topic in self.topics:
            summary = self.agent.execute_task(f"Summarize the document for topic '{topic}':\n{self.text}")
            self.summaries[topic] = summary
        return self.summaries       
    def get_requirements(self):
        for topic in self.topics:
            requirements = self.agent.execute_task(f"Extract detailed requirements for topic '{topic}':\n{self.text}")
        return requirements

    def run_pipeline(self):
        #TODO: Combine all these components and form Processed_Req objects from them and save to REQUIREMENTS dict in storage
        self.process_req_document()
        # Summaries
        self.summarize()
        # Detailed requirements
        reqs = self.get_requirements()
