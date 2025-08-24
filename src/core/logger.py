import os
import logging

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging once
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "carbon_news.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)

def get_logger(name: str = "carbon-news") -> logging.Logger:
    """Get a named logger instance."""
    return logging.getLogger(name)
