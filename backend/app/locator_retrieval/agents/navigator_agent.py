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
        If the whole task is complete, respond with action 'finish'. If some step of the task is completed mark it as done.
        Your response must be a single JSON object with a list of 'actions' and 'updated_task'.
        Example for click: {"updated_task": "1. Navigate to tickets (done)\n2. Choose student...", "actions": [{"action": "click", "css": "a[href='/tickets']", "description": "Navigate to tickets page."}]}
        Example for press_enter: {"updated_task": "1. Enter search query (done)\n2. Click search...", "actions": [{"action": "press_enter", "css": "input[name='q']", "description": "Submit search query."}]}
        Example for goto: {"updated_task": "1. Navigate to home (done)\n2. ...", "actions": [{"action": "goto", "url": "https://www.hsl.fi/en", "description": "Navigate to home page."}]}
        Example for finish: {"updated_task": "1. ... (done)\n2. ... (done)", "actions": [{"action": "finish", "reason": "The ticket price has been found."}]}
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