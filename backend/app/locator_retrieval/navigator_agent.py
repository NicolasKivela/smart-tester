
from app.common.base_agent import BaseAgent



class NavigatorAgent(BaseAgent):
    
    def _get_system_message(self):
        return ("""
        You will be given all the relevant found locators and the task list. Your job is to decide what parts of the task are already done and what could be the next logical step to complete the task list. 
        Choose the relevant locator and action to take using that locator. Available actions are 'click', 'fill', and 'press_enter'. This should be in the outputs action part.
        - 'click': Clicks an element using the locator.
        - 'fill': Fills an element with the given text.
        - 'press_enter': Simulates pressing the Enter key. This can be done on a specific element (if a selector is provided) or on the page in general (if no selector is provided).
        Dont include any reasoning or other explanations. Only return the json output. Use only the the already given locators.
        If the task is about login use provided username and password.
        Don't click the cookie button.
        Use Xpath if possible.
        Return the information as valid json:
        {
        "actions": [
            {
            "action": "<action>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "possible text" : "<text to be filled>"    
            },
            {
            "action": "press_enter",
            "css": "<optional CSS selector or N/A>",
            "xpath": "<optional XPath selector or N/A>"
            }
        ]
        }                
            """)
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}
    
    
    