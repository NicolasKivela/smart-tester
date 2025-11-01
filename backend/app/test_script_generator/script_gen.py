"""
Author: Kalle Hirvijärvi - kalle.hirvijarvi@tuni.fi

Generates robotframework test scripts from BDD-scenarios, login information
and locators by calling LLM agent. Assembles all outputs to a single string
"""

import json

from app.test_script_generator.script_gen_agent import ScriptGenAgent

SECTION_MARKER_START_INDEX = 3
MIN_VARIABLE_SPACE = 4


class ScriptGen:

    def __init__(self):
        """
        Constructor: initializes internal attributes
        Used to temporarily hold LLM output during execution
        """
        self.__keywords = set()   # used to detect duplicates
        self.__keywords_str = ""  # used to store in order
        self.__variables = {}
        self.__scripts = []
        self.__variable_offset = 0

        self.__init_keywords()


    def generate_script(self, features, locators, login):
        """
        Top level public method - returns robotframework test scripts from
        BDD-scenarios and locators by calling LLM agent
        :param features: Feature data as: list[Processed_req])]
        :param locators: target locators as JSON
        :return: result: robotframework test script as JSON object
        """

        for feature in features:
            response = self.__call_agent(feature, locators, login)
            self.__collect_keywords(response)
            self.__collect_variables(response)
            self.__scripts.append(response)

        return self.__assemble_result()

    def __init_keywords(self):
        """
        Initializes setup and teardown keywords to internal attributes
        """

        self.__keywords_str = (
            "Open browser to front page\n"
            "   Open Browser    ${URL}    ${BROWSER}\n"
            "   Maximize Browser Window\n"
            "   Wait Until Page Contains Element    ${ACCEPT_COOKIES_BUTTON}    timeout=10s\n"
            "   Click Element    ${ACCEPT_COOKIES_BUTTON}\n"
            "   Wait Until Element Is Not Visible    ${ACCEPT_COOKIES_BUTTON}    timeout=5s\n\n"
        )
        self.__keywords = {"Open browser to front page\n"}

    def __collect_keywords(self, response):
        """
        saves keywords into internal attributes from robotframework script
        (does not save duplicates)
        :param response: LLM response as string
        """
        response_lines = response.splitlines(True)
        keywords_found = False

        # Finds keyword starting point
        while response_lines:
            line = response_lines.pop(0)
            if "***Keywords***" in line or "*** Keywords ***" in line:
                keywords_found = True
                break

        if not keywords_found:
            print("Warning: No keywords found.")
            return

        new_keyword = ""
        is_new_keyword = False
        for line in response_lines:

            # ignore comments
            if line[0] == "#":
                continue
            elif line == "":
                continue
            # new keyword begins
            elif line[0] != " ":
                # save current
                if new_keyword and new_keyword != "\n":
                    self.__keywords_str += new_keyword + "\n"
                    new_keyword = ""
                # check for duplicate
                if line not in self.__keywords:
                    is_new_keyword = True
                    new_keyword = line
                    self.__keywords.add(new_keyword)

                else:
                    is_new_keyword = False
            # save line if part of new keyword
            else:
                if is_new_keyword:
                    new_keyword += line
        self.__keywords_str += new_keyword + "\n"
    def __collect_variables(self, response):
        """
        saves variables into internal attributes from robotframework script
        (does not save duplicates)
        :param response: LLM response as string
        """

        response_lines = response.splitlines(True)
        variables_found = False

        # Finds variables starting point
        while response_lines:
            line = response_lines.pop(0)
            if "***Variables***" in line or "*** Variables ***" in line:
                variables_found = True
                break

        if not variables_found:
            print("Warning: No variables found.")
            return

        for line in response_lines:
            # new section begins (no more variables)
            if "***" in line:
                return
            # ignore comments
            elif line[0] == "#":
                continue
            # new variable
            elif line:
                line_elements = line.split(" ")
                name = line_elements.pop(0)
                value = " ".join(line_elements)
                name = name.strip()
                value = value.strip()
                # update variable offset
                if len(name) > self.__variable_offset:
                    self.__variable_offset = len(name)
                # check for duplicate mismatch
                if name in self.__variables and self.__variables[name] != value:
                    print("Warning: variable duplicate value mismatch;", name, value)
                else:
                    self.__variables[name] = value

    def __assemble_result(self):
        """
        assembles all LLM responses into a single script and removes duplicate
        settings
        :return: result: robotframework test script as JSON object
        """

        result = ""
        settings = set()
        settings_ordered = []
        tests = ""

        for script in self.__scripts:
            lines = script.splitlines(True)
            phase = "U"
            while lines:
                line = lines.pop(0)
                # new section begins
                if line == "```robotframework\n":
                    continue
                elif line[:SECTION_MARKER_START_INDEX] == "***":
                    phase = line[SECTION_MARKER_START_INDEX]
                    if phase == " ":
                        phase = line[SECTION_MARKER_START_INDEX + 1]
                    # S: Settings
                    # V: Variables
                    # T: Test Cases
                    # K: Keywords
                    # U: undefined - no section marker found
                    # other: unexpected section marker
                elif "Documentation" in line and phase == "S":
                    pass
                else:
                    match phase:
                        case "S":
                            # check for duplicate
                            if line not in settings:
                                settings.add(line)
                                settings_ordered.append(line)
                        case "V":
                            # already saved
                            pass
                        case "T":
                            tests += line
                        case "K":
                            # already saved
                            # last section: no need to continue
                            break
                            # Print warnings instead of raising exception (for now)
                        case "U":
                            #raise RuntimeError("'***' not found")
                            print("waring: '***' not found")
                        case _:
                            #raise RuntimeError("Unexpected text after: '***'")
                            print("waring: unexpected text after: '***':", phase)


        # build final result

        result += "\n*** Settings ***\n"
        for settings_line in settings_ordered:
            result += settings_line

        self.__variable_offset += MIN_VARIABLE_SPACE
        result += "\n*** Variables ***\n"
        for variable in self.__variables.keys():
            result += variable + (self.__variable_offset - len(variable)) * " " + self.__variables[variable] + "\n"

        result += "\n*** Test Cases ***\n" + tests
        result += "\n*** Keywords ***\n" + self.__keywords_str

        # clear internal attributes

        self.__scripts.clear()
        self.__variables.clear()
        self.__init_keywords()
        self.__variable_offset = 0

        # convert to JSON
        return json.dumps({"test_script": result})


    def __call_agent(self, feature, locators, login):
        """
        Assembles input to a single string and calls LLM-agent
        :param feature: Feature as Processed_Req
        :param locators: All known locators as JSON
        :param login: known valid login information as JSON
        :return: LLM response as string
        """
        feature_desc = str(feature.summary)
        scenarios = str(feature.bdd_scenarios)

        LLM_input = (
            "Feature to be tested:\n\n" + feature_desc +
            "\nBDD scenarios:\n\n" + scenarios +
            "\nLocators as JSON:\n\n" + json.dumps(locators) +
            "\nUsable keywords:\n\n" + self.__keywords_str +
            "\nLogin information as JSON:\n\n" + str(login)
        )
        agent_obj = ScriptGenAgent()
        return agent_obj.execute_task(LLM_input)
