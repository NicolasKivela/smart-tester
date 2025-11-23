"""
Author: Kalle Hirvijärvi - kalle.hirvijarvi@tuni.fi

Generates robotframework test scripts from BDD-scenarios, login information
and locators by calling LLM agent. Assembles all outputs to a single string
"""

import json
import traceback
from app.test_script_generator.script_gen_agent import ScriptGenAgent

SECTION_MARKER_START_INDEX = 3
MIN_VARIABLE_SPACE = 4

MAX_WRONG_WORDS = 2
MIN_MATCHING_WORD_COUNT_TO_FIX = 3

BDD_PREFIXES = {
    "And",
    "Then",
    "When",
    "Given"
}

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

        self.__variable_offset = 0      # used to align variable values in final output
        self.__id_storage = set()       # used to store IDs to prevent duplicate API calls
        self.__no_new_scripts = True    # is set to false if API call is made
        self.__temp_case_lines = set()
        self.__failed_keyword_counter = 0

        self.__init_keywords()

    async def generate_script(self, features, bdd_scenarios, locators, login, url):
        """
        Top level public method - returns robotframework test scripts from
        BDD-scenarios and locators by calling LLM agent
        :param features: Feature data as: list[Processed_req]
        :param locators: target locators as JSON
        :return: result: robotframework test script as JSON object
        """
        try:
            self.__no_new_scripts = True

            for feature in features:
                # does not run feature with duplicate ID
                if feature.id in self.__id_storage:
                    continue

                # save id to prevent future duplicate and run
                self.__id_storage.add(feature.id)

                response = await self.__call_agent(feature,bdd_scenarios,locators,login,url)
                try: 
                    if response["status_code"] == 400:
                        return {"status_code": 400, "detail":f"Error response from the model{e}"} 
                except:
                    print("model succesfully responses")
                self.__no_new_scripts = False
                # collect and validate keywords
                self.__failed_keyword_counter = 0
                self.__temp_collect_test_lines(response)
                number_of_case_lines = len(self.__temp_case_lines)
                self.__collect_keywords(response)
                # if there are no test cases or more than half
                # of the keywords do not match any test case lines - try again once

                if number_of_case_lines == 0:   # avoid dividing by 0
                    number_of_case_lines = 1
                    self.__failed_keyword_counter += 1
                if float(self.__failed_keyword_counter) / float(number_of_case_lines) > 0.5:
                    # initialize attributes
                    self.__temp_case_lines.clear()
                    self.__scripts.clear()
                    self.__variables.clear()
                    self.__init_keywords()
                    self.__variable_offset = 0
                    print("Warning: generation failed, trying again...")

                    # try again
                    response = await self.__call_agent(feature,bdd_scenarios,locators, login,url)
                    self.__failed_keyword_counter = 0
                    self.__temp_collect_test_lines(response)
                    self.__collect_keywords(response)

                # continues normally regardless of what happened before
                self.__temp_case_lines.clear()
                self.__collect_variables(response)
                self.__scripts.append(response)

            return {"status_code":200,"detail":"Scripts generated succesfully","body":self.__assemble_result()}
        except Exception as e:
            tb = traceback.format_exc()
            print("Error:", e)
            print("Traceback:\n", tb)
            return {"status_code": 400, "detail":f"Error while generating test scripts: {e}"}

    def __init_keywords(self):
        """
        Initializes hard-coded setup keyword to internal attributes
        """

        self.__keywords_str = (
            "Open browser to front page\n"
            "   Open Browser    ${URL}    ${BROWSER}\n"
            "   Maximize Browser Window\n"
            "   Wait Until Page Contains Element    ${LOC_ACCEPT_COOKIES_BUTTON}    timeout=10s\n"
            "   Click Element    ${LOC_ACCEPT_COOKIES_BUTTON}\n"
            "   Wait Until Element Is Not Visible    ${LOC_ACCEPT_COOKIES_BUTTON}    timeout=10s\n\n"
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
                    new_keyword = self.__validate_keyword(new_keyword)
                    self.__keywords.add(new_keyword)

                else:
                    is_new_keyword = False
            # save line if part of new keyword
            else:
                if is_new_keyword:
                    new_keyword += line

        self.__keywords_str += new_keyword + "\n"

    def __validate_keyword(self, keyword, auto_add_the = False):
        """
        Automatically fixes keyword to match the closest line in test cases
        If there are less that 3 matching words or fixing requires more than 2
        new words, returns keyword parameter as is
        param: keyword, the keyword to be modified
        param: auto_add_the, if true automatically tries to add 'the ' at the beginning of the keyword
        returns: modified keyword if success, and keyword parameter if failure
        """

        if len(keyword) <= 1:
            return keyword
        # check if keyword is already valid
        if keyword.lower() in self.__temp_case_lines:
            self.__temp_case_lines.remove(keyword.lower())
            return keyword

        # auto add "the " (common known problem)
        if keyword.lower()[0:4] != "the " and auto_add_the:
            keyword = "The " + keyword
            if keyword.lower() in self.__temp_case_lines:
                print("Successful keyword validation")
                return keyword

        # finds out the number of common words with each test case line and stores them to a list
        # each index corresponds to a test case line
        keyword_words = keyword.split(" ")
        matching_words = []
        case_lines_list = list(self.__temp_case_lines)
        for case_line in case_lines_list:
            case_line_words = case_line.split(" ")
            case_line_words_set = set(case_line_words)

            num_of_matching_words = 0
            for word in keyword_words:
                if word.lower() in case_line_words_set:
                    num_of_matching_words += 1

            matching_words.append(num_of_matching_words)

        # use the with the most matching words
        max_num_of_matching_words = max(matching_words)##ERROR HERE matching words empty
        best_word_index = matching_words.index(max_num_of_matching_words)

        # validates only if there are at least 3 mathing words and at most 2 new added words
        if max_num_of_matching_words >= MIN_MATCHING_WORD_COUNT_TO_FIX and \
                len(keyword_words) - max_num_of_matching_words <= MAX_WRONG_WORDS:

            print("Successful keyword validation")
            return case_lines_list[best_word_index]
        else:
            if not auto_add_the:
                # recursively tries again (only once) by adding "the " at the beginning
                keyword = self.__validate_keyword(keyword, True)
            # if validation fails:
            print("Waring: Failed keyword:", keyword)
            self.__failed_keyword_counter += 1
            return keyword

    def __temp_collect_test_lines(self, response):
        """
        Stores all test case lines in to set (test case names not included)
        param: response, robotframework script API response
        """

        test_cases_found = False
        response_lines = response.splitlines(True)

        # finds the testcase starting point
        while response_lines:
            line = response_lines.pop(0)
            if "***Test Cases***" in line or "*** Test Cases ***" in line:
                test_cases_found = True
                break

        if not test_cases_found:
            print("Warning: Test Cases found.")
            return

        while response_lines:
            line = response_lines.pop(0)
            # end condition
            if "***" in line:
                return
            # ignore empty
            if len(line) <= 1:
                continue
            # ignore test case names
            if line[0] != " ":
                continue
            # remove BDD prefix
            line = line.strip()
            lines = line.split(" ")
            prefix = lines.pop(0)
            line = " ".join(lines)
            if prefix not in BDD_PREFIXES:
                line = prefix + " " + line

            self.__temp_case_lines.add(line.lower() + "\n")

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
                            print("waring: '***' not found")
                        case _:
                            print("waring: unexpected text after: '***':", phase)


        # build final result

        result += "\n*** Settings ***\n"
        for settings_line in settings_ordered:
            result += settings_line

        self.__variable_offset += MIN_VARIABLE_SPACE
        result += "*** Variables ***\n"
        for variable in self.__variables.keys():
            result += variable + (self.__variable_offset - len(variable)) * " " + self.__variables[variable] + "\n"

        result += "\n*** Test Cases ***\n" + tests
        result += "*** Keywords ***\n" + self.__keywords_str

        # clear internal attributes

        self.__scripts.clear()
        self.__variables.clear()
        self.__init_keywords()
        self.__variable_offset = 0

        if self.__failed_keyword_counter > 0:
            print("Warning:", self.__failed_keyword_counter, "failed keywords")

        if self.__no_new_scripts:
            return None
        else:
            # convert to JSON
            return json.dumps({"test_script": result})


    def __call_agent(self, feature, bdd_scenarios, locators, login, url):
        """
        Assembles input to a single string and calls LLM-agent
        :param feature: Feature as Processed_Req
        :param locators: All known locators as JSON
        :param login: known valid login information as JSON
        :return: LLM response as string
        """
        feature_desc = str(feature.summary)
        scenarios = str(bdd_scenarios)
        str_url = str(url)
        locators_str = str(locators)
        LLM_input = (
            "Feature to be tested:\n\n" + feature_desc +
            "\nURL tested web application:\n\n" + str_url +
            "\nBDD scenarios:\n\n" + scenarios +
            "\nLocators as JSON:\n\n" + locators_str +
            "\nUsable keywords:\n\n" + self.__keywords_str +
            "\nLogin information as JSON:\n\n" + str(login)
        )
        agent_obj = ScriptGenAgent()
        return agent_obj.execute_task(LLM_input)
        
