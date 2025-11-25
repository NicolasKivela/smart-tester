from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class LocatorRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(model=AgentConfig.LocatorRetrievalAgent.model, max_tokens=AgentConfig.LocatorRetrievalAgent.max_tokens)
    
    def _get_system_message(self):
        return AgentConfig.LocatorRetrievalAgent.system_message
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}