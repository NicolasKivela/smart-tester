#"moonshot/kimi-k2-turbo-preview"
#"moonshot/moonshot-v1-32k"
moonshot = "moonshot/kimi-k2-0711-preview"

gemini_lite = "gemini/gemini-2.5-flash-lite"
class AgentConfig:
    class BaseAgent:
        model =  "moonshot/moonshot-v1-32k"
        temperature = 0.1
        max_tokens = 32000
        timeout = 3000
        max_tool_calls = 5

    class RequirementAgent:
        model = "moonshot/moonshot-v1-32k"
        max_tokens = 32000
        system_message = (
            "You are an intelligent assistant that analyzes software requirement documents. "
            "You detect topics, summarize them, and extract detailed requirements."
            "Always output clear, structured, and concise responses."
            "Do not translate the content."
        )

    class ScriptGenAgent:
        model = gemini_lite
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
        model = moonshot
        max_tokens = 100000
        system_message = (
            """You are a senior Test Automation Engineer.
        You will be given scraped locators and the BDD scenarios related to the navigation plan and the current URL.
        Your task is to identify potential locators that could be needed, if one wanted to make test scripts from those scenarios given. Create either xpath and/or css to that locator that could be used in test automation scripts. 
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
        model = moonshot
        max_tokens =100000
        use_aria_snapshot = True
        use_screenshot = True
        record_video = False
        system_message = (
            """
        You will be given all the relevant found locators and the task list. Your job is to decide what parts of the task are already done and what could be the next logical step to complete the task list. Most pages have some cookie acceptance in the first page, so make sure to accpet all cookies before continuing navigation. If you see that there is no cookies questioned ignore this. 
        
        You must also track the progress of the task. If a step in the task list is completed, mark it with "(done)" at the end of the line. Return the updated task list in the "updated_task" field.

        Choose the relevant locator and action to take using that locator. Available actions are 'click', 'fill', 'press_enter', and 'goto'.
        - 'click': Clicks the element using the locator.
        - 'fill': Fills the element chosen by the selector with the text given.
        - 'press_enter': Simulates pressing the Enter key on the element.
        - 'goto': Navigates to a specific URL. Use this only when you find yourself stuck on wrong page. This way you can reset your session in a way and start again.
        Dont include any reasoning or other explanations. Only return the json output. 
        Return the information as valid json:
        {
        "updated_task": "<the full task list with completed steps marked as (done)>",
        "actions": [
            {
            "action": "<action>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>",
            "possible text" : "<text to be filled>"    
            }
        ]
        }                
            """
        )

    class BDDTaskAgent:
        model = moonshot
        max_tokens = 32000
        system_message = (
            """ 
    You are a web automation planning expert.

    You receive one or more BDD scenarios and a URL. 
    Your job is to plan a single efficient route through the website that satisfies ALL BDD scenarios 
    with the minimum number of steps. Clearly define the last step of the plan. Based on the last part the task list can be stated as finished.
    Last step of the plan should be like 'finish, when you have completed all the tasks'.

    Purpose of the plan is to make route to get all relevant locators for the bdd scenarios using this navigation plan.
    
    Plan must be numerated steps for example:
    1. 
    2.
    3.
    ...
    Only include the plan in your answer not include explanation or reasoning.
    """
        )

    class BDDGenerationAgent:
        model = moonshot
        max_tokens = 32000
        system_message = (
            "You are a BDD Scenario Generator Agent. Your task is to generate comprehensive Behavior-Driven Development (BDD) scenarios in Gherkin syntax based on the provided feature and its related requirements."
            "Input:"
            "- Feature: A short description of the functionality."
            "- Requirements: A list of system requirements parsed from a specification document that relate to the feature."
            "Instructions:"
            "- Generate multiple BDD scenarios that together cover all the provided requirements as thoroughly as possible."
            "- Use Gherkin syntax: `Scenario:`, `Given`, `When`, `Then`, and `And` (if needed)."
            "- Do not include any explanation, metadata, or commentary—only output the scenarios."
            "- Each scenario should be clear, concise, and focused on one behavior or requirement."
            "- If requirements overlap, group them logically into a single scenario where appropriate."
            "Output:"
            "Only the Gherkin scenarios."
            "Example input:"
            "Feature: User login"
            "Requirements:"
            "- The system must allow users to log in using email and password."
            "- The system must lock the account after 5 failed login attempts."
            "- The system must show an error message for incorrect credentials."
            "Expected output:"
            "Scenario: Successful login with valid credentials"  
            "Given the user is on the login page"  
            "When the user enters a valid email and password"  
            "Then the user should be redirected to the dashboard"  
            "Scenario: Failed login with incorrect credentials"  
            "Given the user is on the login page"  
            "When the user enters an incorrect password"  
            "Then an error message should be displayed"  
            "Scenario: Account lock after multiple failed attempts"  
            "Given the user has failed to log in 5 times"  
            "When the user attempts to log in again"
            "Then the account should be locked"  
            "And a message should inform the user about the lock"
        )
