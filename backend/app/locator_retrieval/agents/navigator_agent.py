from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class NavigatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(model=AgentConfig.NavigatorAgent.model, max_tokens=AgentConfig.NavigatorAgent.max_tokens)
    
    def _get_system_message(self):
        return AgentConfig.NavigatorAgent.system_message
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}