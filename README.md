# smart-tester
Smart testing tool for software engineering project course.


##  Getting Started

### 1. Clone the Repository

   

### 2. Run with Docker
Download docker desktop
Build the containers:
    docker compose build

Start the containers:
    docker compose up

The service should now be running locally.

---

##  Usage

- API documentation: http://localhost:8000/docs

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
The output of this program is robotframework test scripts. (for more infirmation go to https://robotframework.org/ or https://github.com/robotframework/robotframework) In order to run them the text needs to be copied to .robot file and ran.

## Requirements for running:
- Python 3.8 (or newer)
- Google Chrome - you can also use a diffferent browser by changing the ${BROWSER} variable's value to something else from the script so really any web browser is fine
- Robotframework and selenim library python backages

### Installing packages with pip

For this you need to have python and and pip installed.

Run following commands:

    pip install robotframework
    pip install robotframework-seleniumlibrary

## Run scripts

- Copy the output text in to a .robot file (or in to a .txt and then change it to .robot file) This can be done with any code editor.
- Run the file with robot command

like this:

    robot <path>/<filname>.robot    

for example, if your file is testrun.robot and the file in the current working directory, run:

    robot testrun.robot



