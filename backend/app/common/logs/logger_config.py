import logging
import os
import traceback


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
        #logging.StreamHandler()  # shows in consol
    ]
)

logger = logging.getLogger("ai_agent_logger")

def reset_logs():
    """
    Clears the content of the log file.
    Returns 200 on success, 400 on error.
    """
    try:
        # Just to be extra safe: make sure the directory exists
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Try to truncate / recreate the file
        with open(LOG_FILE, "w", encoding="utf-8"):
            pass

        print(f"Logs cleared: {LOG_FILE}")
        return 200

    except Exception as e:
        error_type = type(e).__name__
        error_msg = f"{error_type}: {e}"
        print(f"Error clearing logs for {LOG_FILE}: {error_msg}")
        # This prints full traceback to console so you can see *exactly* what happened
        traceback.print_exc()
        return 400