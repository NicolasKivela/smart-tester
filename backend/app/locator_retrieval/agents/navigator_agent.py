from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class NavigatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(model=AgentConfig.NavigatorAgent.model, max_tokens=AgentConfig.NavigatorAgent.max_tokens)
        self.use_aria_snapshot = getattr(AgentConfig.NavigatorAgent, 'use_aria_snapshot', False)
        self.use_screenshot = getattr(AgentConfig.NavigatorAgent, 'use_screenshot', False)
    
    def _get_system_message(self):
        return AgentConfig.NavigatorAgent.system_message
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}

    def construct_prompt(self, task: str, history: list, locators: dict, aria_snapshot: str = None, screenshot: str = None):
        """
        Constructs the prompt for the NavigatorAgent, optionally including aria-snapshot and screenshot.
        """
        prompt_text = f'''
        Overall Task: {task}

        Action History (what has been done so far):
        {history}

        Locators found on the CURRENT page:
        {locators}
        '''

        if self.use_aria_snapshot and aria_snapshot:
            prompt_text += f'''
            
            Aria Snapshot (Accessibility Tree):
            {aria_snapshot}
            '''

        prompt_text += '''
        Based on the task, history, and current page locators (and aria snapshot if provided), what is the single next action to perform?
        Provide a robust CSS or XPath selector.
        If the task is complete, respond with action 'finish'.
        Your response must be a single JSON object with a list of 'actions'.
        Example for click: {"actions": [{"action": "click", "css": "a[href='/tickets']", "description": "Navigate to tickets page."}]}
        Example for finish: {"actions": [{"action": "finish", "reason": "The ticket price has been found."}]}
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