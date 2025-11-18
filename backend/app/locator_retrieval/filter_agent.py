from app.common.base_agent import BaseAgent



class FilterAgent(BaseAgent):
    
    def _get_system_message(self):
        return ("""You will work as a filter
        You will be given a list of scraped locators.
        Your task is to identify locators that are dublicated in the list and remove those duplicates.
        The duplicate might have different description but it might still be the same locator. 
        Remove also locators that has N/A as a css and xpath.
        Otherwise keep the format exactly same.
        If there are no duplicate locators don't do anything.
        Return only valid JSON in this format:
        {
        "locators": [
            {{
            "description": "<short readable name>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "locator found from": "<url>"   
            }}
        ]
        }
        """)
        
    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}
    