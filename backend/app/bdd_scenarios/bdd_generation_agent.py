"""
Author: Mikael Alamäki

Implementation for abstract BaseAgent class:
Gives the right context to LLM-agent for bdd scenario generation
"""
from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig

class   BddGenerationAgent(BaseAgent):
    def __init__(self, session_id: str):
        super().__init__(model=AgentConfig.BDDGenerationAgent.model,
                        max_tokens=AgentConfig.BDDGenerationAgent.max_tokens,
                        session_id=session_id, agent="bdd_agent")
        
    def _get_system_message(self):
        return AgentConfig.BDDGenerationAgent.system_message
    
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}