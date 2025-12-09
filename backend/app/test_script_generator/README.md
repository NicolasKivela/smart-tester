## Script generator warnings

The script generator will print warnings if there's some problem with parsing the API response but will try to keep going so that issues with the code can be fixed manually Here's all possible warnings, their cause and associated behavior:

### no <keywords/test cases/variables> found:
Cause: response does not have section marker e.g. "*** Keywords ***" (version without spaces also accepted)

Behavior: continues normally - will most likely return empty or invalid script


### '***' not found
Cause: '***' is not found from the first line of API response (warning for every line section marker is not found)

Behavior: does not parse anything from the response until valid section marker is found


###  unexpected text after '***': <first letter after  ***>
Cause: the first letter after ' *** ' is not S/V/T/K

Behavior: does not parse anything from the response until valid section marker is found


### variable duplicate value mismatch: <*variable name*>
Cause: different API calls generate variables with same name but different values

Behavior: the first value is used and other(s) are lost (will not cause issues if caused by having different locators for same element)


### Failed keyword: <*keyword name*>
Cause: response has keyword name that doesn't match any line in test cases and self healing fails

Behavior: the result will have a keyword that is never called


### Successful keyword validation
Cause: same as above but automatic self healing is successful

Behavior: there should be no issues (in an extremely rare case, some keywords could get mixed up there is only 1- or 2-word difference)


### <*number of failed keywords*> failed keywords
Cause: Failed keyword warning is triggered once or more

Behavior: the result will have a keyword(s) that are never called

### generation failed, trying again...
Cause: more than 20% of keywords fail or no test cases are found or API returns http status code that starts with 5

Behavior: will try again once, after second try will return normal result or http response if API returns error

