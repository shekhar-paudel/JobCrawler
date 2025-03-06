import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "jobcrawler.log")

# Create a logger
logger = logging.getLogger("jobcrawler")
logger.setLevel(logging.INFO)  # Change to DEBUG for more details

# Log format
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Console Handler (prints logs to the console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# File Handler with Log Rotation (5MB per file, keeps last 5 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
