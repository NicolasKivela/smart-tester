"""
Author: Kalle Hirvijärvi

Implementation for abstract BaseAgent class:
Gives the right context to LLM-agent for test script generation
"""

from app.common.base_agent import BaseAgent


class ScriptGenAgent(BaseAgent):

    def __init__(self):
        # increased max tokens for script generation
        super().__init__(max_tokens= 32768)

    def _get_system_message(self):
        return (
            "Your job is to write test test scripts for web applications using robotframework. "
            "Write atleast one test case per scenario. "
            "Generate the test scripts based on the given BDD-scenarios"
            "You are also given login information that can be used if needed. "
            "You are given a list of locators. to use. If a needed locator is not provided, use |@| as placeholder. "
            "Do not generate any locator that you aren't specifically given. "
            "You can use previously generated keywords that you are given, or generate new ones if needed. "
            "You can use selenium library but no other external libraries. "
            "Use 'Open browser to front page' and 'Close browser' keywords as test setup and test teardown. "
            "Do not make other setup or teardown keywords. "
            "Include all Test cases and keywords in a single file and do not utilize a .resource file. "
            "Only answer with code. Use BDD format. "
            "Make the result in order: settings, variables test cases, keywords"
        )

    def _get_tools(self):
        return None

    def _get_tool_functions(self):
        return None
