from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class BDDTaskAgent(BaseAgent):
    def __init__(self):
        super().__init__(model=AgentConfig.BDDTaskAgent.model, max_tokens=AgentConfig.BDDTaskAgent.max_tokens)
   
    def _get_system_message(self):
        return AgentConfig.BDDTaskAgent.system_message

    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}