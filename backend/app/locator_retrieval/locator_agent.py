from .scraper import scrape_interactive_elements
from app.common.base_agent import BaseAgent



class LocatorRetrievalAgent(BaseAgent):
    
    def _get_system_message(self):
        return ("""You are a senior Test Automation Engineer using Playwright.

        Your task is to identify **all locators in the path that are needed** following the plan and to create either xpath and/or css to that locator that could be used in test automation scripts. 
        Use the tool given to scrape interactive elements and generate the relevant locators by using the output. Try to create as robust locators as you can, so that test automation scripts do not fail to some locators resulting multiple elements.
        If some locators are not found, do not make them up yourself, just dont return anything, if you cant find relevant locators.
        Stop prosessing when the plan has come to an end
        Return only valid JSON in this format:
        {{
        "locators": [
            {{
            "description": "<short readable name>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>"
            }}
        ]
        }}

        """)
        
    def _get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "scrape_interactive_elements",
                    "description": "Scrapes a URL and returns a list of interactive HTML elements.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to scrape."
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]
    
    def _get_tool_functions(self):
        return {
                "scrape_interactive_elements": scrape_interactive_elements
            }
    
    
    