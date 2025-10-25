from scraper import scrape_interactive_elements
from app.common.base_agent import BaseAgent



class LocatorRetrievalAgent(BaseAgent):
    
    def _get_system_message(self):
        return ("""You are a senior Test Automation Engineer using Playwright.


        I have scraped all interactive elements and here is the raw HTML for them.
        Please identify **all locators in the path that are needed** following the plan, including:
        - main menu buttons
        - category links
        - product links
        - add-to-cart buttons
        - next navigation steps
        -etc
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
                    "description": "return parsed html with interactive elements",
                }
            }
        ]
    
    def _get_tool_functions(self):
        return {
                "scrape_interactive_elements": scrape_interactive_elements
            }
    
    
    