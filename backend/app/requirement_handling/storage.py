# temporary storage
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
        bdd_scenarios={}
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
        bdd_scenarios={}
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
        bdd_scenarios={}
    )
}
