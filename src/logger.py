import logging
import os
from datetime import datetime

# Generate a timestamp
timestamp = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

# Create logs directory
LOGS_BASE_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_BASE_DIR, exist_ok=True)

# Create a subfolder with the timestamp
LOG_FOLDER = os.path.join(LOGS_BASE_DIR, timestamp)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Create the log file inside that folder (with same name as folder)
LOG_FILE = f"{timestamp}.log"
LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Test log (you can comment this out later)
if __name__ == "__main__":
    logging.info("Logging has been set up in timestamped folder.")
