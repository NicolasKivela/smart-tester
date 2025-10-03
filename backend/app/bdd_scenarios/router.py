from fastapi import APIRouter
router = APIRouter()

@router.get("/bdd_scenarios",tags=["bdd_scenarios"])
async def read_bdd_scenarios():
    json=[
  {
    "id": 1,
    "feature": "Login",
    "scenario": "Successful login with valid credentials",
    "given": [
      "a registered user with email 'user@example.com' and password 'Password123'"
    ],
    "when": [
      "the user submits a login request with correct credentials"
    ],
    "then": [
      "the system responds with a 200 status",
      "a JWT access token is returned",
      "the user is redirected to the dashboard"
    ]
  },
  {
    "id": 2,
    "feature": "CRM Contact Management",
    "scenario": "Add a new contact to a company",
    "given": [
      "a company 'Acme Inc.' exists in the CRM"
    ],
    "when": [
      "the user submits a new contact with name 'Jane Doe' and email 'jane@acme.com'"
    ],
    "then": [
      "the contact is stored in the CRM",
      "the contact is linked to 'Acme Inc.'",
      "the system returns a success message"
    ]
  },
  {
    "id": 3,
    "feature": "Survey Automation",
    "scenario": "Send survey reminder email",
    "given": [
      "a contact 'John Smith' with email 'john@example.com' exists",
      "a survey is scheduled for John Smith"
    ],
    "when": [
      "the scheduled reminder time is reached"
    ],
    "then": [
      "the system sends a reminder email to 'john@example.com'",
      "the automation log records the reminder as sent"
    ]
  },
  {
    "id": 4,
    "feature": "Dashboard Analytics",
    "scenario": "View project status summary",
    "given": [
      "survey responses have been collected for project 'Website Redesign'"
    ],
    "when": [
      "the user navigates to the dashboard page"
    ],
    "then": [
      "the dashboard displays sentiment analysis of the responses",
      "the project status is shown as 'Good', 'OK', or 'Bad'"
    ]
  }
]
    return json



