from app.common.base_agent import BaseAgent



class BDDTaskAgent(BaseAgent):
   
    def _get_system_message(self):
        return( """ 
    You are a web automation planning expert.

    You receive one or more BDD scenarios and a URL. 
    Your job is to plan a single efficient route through the website that satisfies ALL BDD scenarios 
    with the minimum number of steps.

    Purpose of the plan is to make route to get all relevant locators for the bdd scenarios using the plan.
    
    Plan must be numerated steps for example:
    1. 
    2.
    3.
    ...
    Only include the plan in your answer not include explanation or reasoning.
    """)

    def _get_tools(self):
        return []
    
    def _get_tool_functions(self):
        return {}