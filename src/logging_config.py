import logging
import os

# Dynamically find the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure logs directory exists
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOGS_DIR, "preprocessing.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # File logging
        logging.StreamHandler()  # Print logs to the console
    ]
)

logger = logging.getLogger(__name__)
