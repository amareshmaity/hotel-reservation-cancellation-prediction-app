import logging
import os
from datetime import datetime

## Create log directory
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

## Create files path
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime("%Y-%m-%d")}.log")

## Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

## get logger function
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger