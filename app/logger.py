import logging
import os

# Create a 'logs' directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Setup basic configuration
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("logs/sentinel_system.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SENTINEL-CORE")

# Test log to see if it works immediately on startup
logger.info("--- SENTINEL LOGGER INITIALIZED ---")