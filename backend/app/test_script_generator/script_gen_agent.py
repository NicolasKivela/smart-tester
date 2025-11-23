"""
Author: Kalle Hirvijärvi

Implementation for abstract BaseAgent class:
Gives the right context to LLM-agent for test script generation
"""

from app.common.base_agent import BaseAgent
from app.common.agent_config import AgentConfig


class ScriptGenAgent(BaseAgent):

    def __init__(self):
        # increased max tokens for script generation
<<<<<<< HEAD
        super().__init__(model=AgentConfig.ScriptGenAgent.model, max_tokens=AgentConfig.ScriptGenAgent.max_tokens)
=======
        super().__init__(model="gemini/gemini-2.5-flash", max_tokens= 32768)#model="gemini/gemini-2.5-flash"
>>>>>>> origin/dev

    def _get_system_message(self):
        return AgentConfig.ScriptGenAgent.system_message

    def _get_tools(self):
        return None

    def _get_tool_functions(self):
        return None
