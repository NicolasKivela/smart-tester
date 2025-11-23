class AgentConfig:
    class BaseAgent:
        model = "gemini/gemini-2.5-flash-lite"
        temperature = 0.1
        max_tokens = 32000
        timeout = 3000
        max_tool_calls = 5

    class RequirementAgent:
        model = "gemini/gemini-2.5-flash-lite"
        max_tokens = 32000
        system_message = (
            "You are an intelligent assistant that analyzes software requirement documents. "
            "You detect topics, summarize them, and extract detailed requirements."
            "Always output clear, structured, and concise responses."
            "Do not translate the content."
        )

    class ScriptGenAgent:
        model = "gemini/gemini-2.5-flash"
        max_tokens = 32768
        system_message = (
            "Your job is to write test test scripts for web applications using robotframework. "
            "Write atleast one test case per scenario. "
            "Generate the test scripts based on the given BDD-scenarios. "
            "You are also given login information that can be used if needed. "
            "You are given a list of locators. to use. If a needed locator is not provided, use |@| as placeholder. "
            "Do not generate any locator that you aren't specifically given. "
            "Prefer xpath over css. Give every locator variable name 'LOC' prefix. "
            "Make all input field contents and locators in to variables. "
            "You can use previously generated keywords that you are given, or generate new ones if needed. "
            "Make sure that every line in the BDD scenario test case is a defined keyword. "
            "If testcase starts from the frontpage, verify that frontpage is open. "
            "Do not put any arguments to test cases. "
            "To do that use 'Location Should Contain' keyword "
            "Include 'Wait Until Page Contains' Before 'Click Element' in keywords. "
            "Include timeout argument if necessary. "
            "You can use selenium library but no other external libraries. "
            "Use 'Open browser to front page' as test setup keyword. Use Close browser as test teardown. "
            "Do not make other setup or teardown keywords. "
            "Include all Test cases and keywords in a single file and do not utilize a .resource file. "
            "Only answer with code. Use BDD format. "
            "Make the result in order: settings, variables test cases, keywords"
        )

    class LocatorRetrievalAgent:
        model = "gemini/gemini-2.5-flash-lite"
        max_tokens = 32000
        system_message = (
            """You are a senior Test Automation Engineer.
        You will be given scraped locators and the task and the current URL.
        Your task is to identify **all locators in the path that are needed** following the plan and to create either xpath and/or css to that locator that could be used in test automation scripts. 
        Use the inputted elements and generate the relevant locators by using the input. Try to create as robust locators as you can, so that test automation scripts do not fail to some locators resulting multiple elements.
        If some locators are not found, do not make them up yourself, just dont return anything, if you cant find relevant locators.
        Stop prosessing when the plan has come to an end
        Add also the current url to the output
        Return only valid JSON in this format:
        {{
        "locators": [
            {{
            "description": "<short readable name>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "locator found from": "<url>"   
            }}
        ]
        }}

        """
        )

    class NavigatorAgent:
        model = "gemini/gemini-2.5-flash-lite"
        max_tokens = 32000
        system_message = (
            """
        You will be given all the relevant found locators and the task list. Your job is to decide what parts of the task are already done and what could be the next logical step to complete the task list. 
        Choose the relevant locator and action to take using that locator. Available actions are 'click' and 'fill' and this should be in the outputs action part. Click just simply clicks the element using the locator. Fill fills the element chosen by the selector and fills in the text given. 
        Dont include any reasoning or other explanations. Only return the json output. 
        Return the information as valid json:
        {{
        "actions": [
            {{
            "action": "<action>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "possible text" : "<text to be filled>"    
            }}
        ]
        }}                
            """
        )

    class BDDTaskAgent:
        model = "gemini/gemini-2.5-flash-lite"
        max_tokens = 32000
        system_message = (
            """ 
    You are a web automation planning expert.

    You receive one or more BDD scenarios and a URL. 
    Your job is to plan a single efficient route through the website that satisfies ALL BDD scenarios 
    with the minimum number of steps. Clearly define the last step of the plan. Based on the last part the task list can be stated as finished

    Purpose of the plan is to make route to get all relevant locators for the bdd scenarios using the plan.
    
    Plan must be numerated steps for example:
    1. 
    2.
    3.
    ...
    Only include the plan in your answer not include explanation or reasoning.
    """
        )
