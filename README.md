# smart-tester

An LLM-driven test automation tool for UI and System Testing, that converts software requirements into executable test suites.

- Extracts functional features from raw documentation via LLMs.

- Automatically transforms features into Gherkin/BDD scenarios.

- Uses LLMs to dynamically identify and extract UI elements from target URLs.

- Generates Robot Framework test scripts.

- Integrated token usage monitoring for LLM operations.

https://github.com/user-attachments/assets/4896c8cf-d96f-49a6-90a0-97c4e6fa8703


##  Getting Started

### 1. Clone the Repository
To access the most recent stable version, switch to dev-branch.

### 2. Run with Docker
Download docker desktop
Build the containers:
    docker compose build

Start the containers:
    docker compose up

The service should now be running locally.

---

##  Usage

- API documentation: http://localhost:8010/docs
- App frontend: http://localhost:5174
- To reset the database, press "Reset Session" button in the UI.

## Configurations
- backend/app/common/agent_config.py has configurations for all the different AI agents in our system including their system messages
- Switching models and model providers requires the provideres API key in the .env file. See .env.example for more information about this.

---
## Contribution rules
- Pick or create an issue
- Create new branch following the branching rules
- When finished, create a pull request to the **dev** branch
- **main** branch will be secured for now
---
#  Branching Rules
## Main Branches
- main → production-ready
- dev → integration branch for new work

## Feature Branches
- feature/<frontend|backend>-<short-name>
  Example: feature/frontend-auth-ui

## Fix Branches
- fix/<frontend|backend>-<short-name>
  Example: fix/backend-db-connection

## Hotfix Branches
- hotfix/<short-name>
  Example: hotfix/backend-critical-bug

---

# Running test scripts
The output of this program is robotframework test scripts. Robot framefork is a python based framework for test automation. For more information go to: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html and https://robotframework.org/. In order to run them the output text of the program needs to be copied in to .robot file and ran.

## Requirements for running:
- Python 3.8 (or newer)
- Google Chrome - you can also use a diffferent browser by changing the ${BROWSER} variable's value to something else from the script so really any web browser is fine
- Robotframework and selenim library python backages (more detailed instructions: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#installation-instructions)

### Installing packages with pip

For this you need to have python and and pip installed.

Run following commands:

    pip install robotframework
    pip install robotframework-seleniumlibrary

You might also want to install these packages just to your python virtual environment instead of your global python installation. This ensures that other installations for other projects doesn't break your project (and vise versa).
For more information go to: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment

## Run scripts

- Copy the output text in to a .robot file (or in to a .txt and then change it to .robot file) This can be done with any code editor.
- Run the file with robot command

like this:

    robot <path>/<filename>.robot

for example, if your file is testrun.robot and the file in the current working directory, run:

    robot testrun.robot



