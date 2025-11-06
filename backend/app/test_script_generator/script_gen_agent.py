"""
Author: Kalle Hirvijärvi

Implementation for abstract BaseAgent class:
Gives the right context to LLM-agent for test script generation
"""

from app.common.base_agent import BaseAgent


class ScriptGenAgent(BaseAgent):

    def __init__(self):
        # increased max tokens for script generation
        super().__init__(model="gemini/gemini-2.5-flash", max_tokens= 32768)

    def _get_system_message(self):
        return (
            "Your job is to write test test scripts for web applications using robotframework. "
            "Write atleast one test case per scenario. "
            "Generate the test scripts based on the given BDD-scenarios"
            "You are also given login information that can be used if needed. "
            "You are given a list of locators. to use. If a needed locator is not provided, use |@| as placeholder. "
            "Do not generate any locator that you aren't specifically given. "
            "Prefer xpath over css. "
            "Make all input field contents and locators in to variables. "
            "You can use previously generated keywords that you are given, or generate new ones if needed. "
            "Make sure that every line in the BDD scenario test case is a defined keyword. "
            "If testcase starts from the frontpage, verify that frontpage is open. "
            "To do that use 'Location Should Contain' keyword "
            "Include 'Wait Until Page Contains' Before 'Click Element' in keywords. "
            "You can use selenium library but no other external libraries. "
            "Use 'Open browser to front page' as test setup keyword. Use Close browser as test teardown. "
            "Do not make other setup or teardown keywords. "
            "Include all Test cases and keywords in a single file and do not utilize a .resource file. "
            "Only answer with code. Use BDD format. "
            "Make the result in order: settings, variables test cases, keywords"
        )

    def _get_tools(self):
        return None

    def _get_tool_functions(self):
        return None
