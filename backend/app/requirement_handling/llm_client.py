import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

# Configure API
# Make an .env file and add "GOOGLE_API_KEY=key here "
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model once and reuse
client = genai.GenerativeModel("gemini-2.5-flash")