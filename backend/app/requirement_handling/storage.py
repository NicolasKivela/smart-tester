# temporary storage
import re
from app.requirement_handling.schemas import Processed_Req
REQ_TOPICS = []
REQUIREMENTS = {
    1: Processed_Req(
        id=1,
        feature="Login",
        summary="User authentication with email and password",
        requirements=[
            "User can register with email and password",
            "User can log in with valid credentials",
            "Invalid credentials return error message",
            "Password must be hashed in the database"
        ],
        bdd_scenarios=[
    {
      "id": 1,
      "feature": "Login",
      "scenario": "User registration with email and password",
      "given": [
        "the user is on the registration page"
      ],
      "when": [
        "the user provides a unique email and a password"
      ],
      "then": [
        "a new user account should be created",
        "the user should be able to log in with these credentials"
      ]
    },
    {
      "id": 2,
      "feature": "Login",
      "scenario": "Successful login with valid credentials",
      "given": [
        "a user is registered with email \"test@example.com\" and password \"Password123\"",
        "the user is on the login page"
      ],
      "when": [
        "the user enters \"test@example.com\" as email and \"Password123\" as password",
        "the user clicks the login button"
      ],
      "then": [
        "the user should be successfully logged in",
        "the user should be redirected to the dashboard"
      ]
    },
    {
      "id": 3,
      "feature": "Login",
      "scenario": "Failed login with incorrect credentials",
      "given": [
        "a user is registered with email \"test@example.com\" and password \"Password123\"",
        "the user is on the login page"
      ],
      "when": [
        "the user enters \"test@example.com\" as email and \"WrongPassword\" as password",
        "the user clicks the login button"
      ],
      "then": [
        "an error message \"Invalid email or password\" should be displayed",
        "the user should remain on the login page"
      ]
    }
  ]
    ),
    2: Processed_Req(
        id=2,
        feature="Profile Management",
        summary="Allow users to update personal details",
        requirements=[
            "User can update name, email, and phone number",
            "Email must be unique across all accounts",
            "Profile picture upload supported (JPG, PNG)"
        ],
        bdd_scenarios=[]
    ),
    3: Processed_Req(
        id=3,
        feature="Project Dashboard",
        summary="Display all projects with key metrics",
        requirements=[
            "Projects are listed with name, status, and deadline",
            "Search and filter functionality",
            "Dashboard auto-refresh every 60 seconds"
        ],
        bdd_scenarios=[]
    )
}
REQUIREMENTS={}
class db_requirements():
    def get_req_by_id(id):
        try:
            return REQUIREMENTS[id]    
        except:
            print(f"Requirement by {id} cannot be found")
            return
    def add_bdd_scenarios(feature_id,bdd_scenario):
        try:
            REQUIREMENTS[feature_id].bdd_scenarios.append(bdd_scenario)
            return "bdd_scenarios updated succesfully"
        except:
            print("error when updating requirements data")
            return
    def create_processed_req(processed_reqs, summaries, topics):
        try:
          # Combine all data into Processed_Req objects
          for i, (key, value) in enumerate(processed_reqs.items(),start=1):
              processed = Processed_Req(
                  id=i,
                  feature=key,
                  summary=re.sub(r'^\*\*Topic:.*?\*\*\s*', '', summaries.get(key, ""), flags=re.MULTILINE),
                  requirements=value,
                  bdd_scenarios=[]
              )
              REQUIREMENTS[i] = processed.model_dump()
        except Exception as e:
            print(e)
            print("Error creating new requirements to database")
            
