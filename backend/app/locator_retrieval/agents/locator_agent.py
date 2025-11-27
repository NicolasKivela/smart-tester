from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class LocatorRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(model=AgentConfig.LocatorRetrievalAgent.model, max_tokens=AgentConfig.LocatorRetrievalAgent.max_tokens)
        self.use_aria_snapshot = getattr(AgentConfig.LocatorRetrievalAgent, 'use_aria_snapshot', True)
        self.use_screenshot = getattr(AgentConfig.LocatorRetrievalAgent, 'use_screenshot', False)

    def _get_system_message(self):
        return AgentConfig.LocatorRetrievalAgent.system_message
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}

    def construct_prompt(self, scraped_elements: dict, aria_snapshot: str = None, screenshot: str = None):
        """
        Constructs the prompt for the LocatorRetrievalAgent, including aria-snapshot and optionally screenshot.
        """
        prompt_text = f'''Heres the interactive elements of the page: {scraped_elements}
        and here is the aria snapshot of the page: {aria_snapshot}
        '''

        if self.use_screenshot and screenshot:
            # Multimodal input
            return [
                {
                    "type": "text",
                    "text": prompt_text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{screenshot}"
                    }
                }
            ]
        else:
            return prompt_text    