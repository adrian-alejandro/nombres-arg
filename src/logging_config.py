import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/preprocessing.log"),  # File logging
        logging.StreamHandler()  # Console logging
    ]
)

logger = logging.getLogger(__name__)
