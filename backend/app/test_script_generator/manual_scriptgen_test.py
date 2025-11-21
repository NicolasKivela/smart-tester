
from script_gen import ScriptGen
from backend.app.requirement_handling.schemas import Processed_Req

import json

def main():

    file = open("test_locators.txt")
    locators = file.read()
    file.close()

    login = ' \
    { \
        "username":"0443087766"\
        "password":"jcnl-HFm-F_7xJR"\
        "url":"https://www.hsl.fi" \
    }'

    features = []
    feature_desc = "Basic test scenarios"
    bdd_list = [
    "Scenario: User plans a trip from Helsinki Central Railway Station to Espoo \
        Given the user is on the HSL.fi homepage \
        When the user enters 'Helsinki Central Railway Station' in the 'From' field \
        And the user enters 'Espoo' in the 'To' field \
        Then the system should display a list of route options \
        And each route option should include travel time, modes of transport, and departure times"
        ,
    "Scenario: User checks real-time departures for a stop \
        Given the user is on the HSL.fi homepage \
        When the user searches for stop Rautatientori \
        Then the system should display a list of upcoming departures \
        And each departure should show line number, destination, and minutes until departure"
        ,
    "Scenario: User switches the website language from Finnish to English \
        Given the user is on the HSL.fi homepage \
        And the website content should be displayed in Finnish \
        When the user clicks the in English \
        Then the website content should be displayed in English \
        And the URL should be https://www.hsl.fi/en'"
        ,
    "Scenario: User checks ticket prices for an AB zone \
        Given the user is on the HSL.fi homepage \
        When the user navigates to the 'Tickets and fares' section \
        And the user selects the 'ABC' as zone \
        And the user selects student as customer group \
        And the user presses the show prices button \
        Then the system should display the available ticket types \
        And the correct prices for each ticket type should be visible"
        ,
    "Scenario: User successfully logs into My HSL \
        Given the user is on the HSL.fi homepage \
        When the user clicks the Login button \
        And the login page is displayed \
        And the user enters a valid phone number and password \
        And the user clicks the Submit Login button \
        Then the user menu button should be visible"
    ]
    feature = Processed_Req
    feature.id = 1
    feature.bdd_scenarios = bdd_list
    feature.summary = feature_desc
    features.append(feature)

    gen_obj = ScriptGen()
    result = gen_obj.generate_script(features, locators, login)
    if not result:
        print("This should not happen")

    print("=== BEGIN RESPONSE ===")
    print(json.loads(result)["test_script"])
    print("=== END RESPONSE ===")

if __name__=="__main__":
    main()
