
from app.common.base_agent import BaseAgent



class NavigatorAgent(BaseAgent):
    
    def _get_system_message(self):
        return ("""
        You will be given all the relevant found locators and the task list. Your job is to decide what parts of the task are already done and what could be the next logical step to complete the task list. 
        Choose the relevant locator and action to take using that locator. Available actions are 'click' and 'fill' and this should be in the outputs action part. Click just simply clicks the element using the locator. Fill fills the element chosen by the selector and fills in the text given. 
        Dont include any reasoning or other explanations. Only return the json output. Use only the the already given locators.
        If the task is about login use provided username and password.
        Don't click the cookie button.
        Use Xpath if possible.
        Return the information as valid json:
        {
        "actions": [
            {{
            "action": "<action>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "possible text" : "<text to be filled>"    
            }}
        ]
        }                
            """)
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}
    
    
    