import logging
import os


for name in logging.root.manager.loggerDict:
    if name.startswith("sqlalchemy"):
        logging.getLogger(name).disabled = True
        
# Creates log file
LOG_DIR = os.path.join(os.path.dirname(__file__), "files")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "ai_agent.log")

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # shows in consol
    ]
)

logger = logging.getLogger("ai_agent_logger")