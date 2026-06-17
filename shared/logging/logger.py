from loguru import logger
import os


# -------------------------------
# Create logs directory
# -------------------------------

os.makedirs("logs", exist_ok=True)


# -------------------------------
# Configure Logger
# -------------------------------

logger.add(

    "logs/system.log",

    rotation="10 MB",

    retention="10 days",

    level="INFO",

    enqueue=True
)


logger.add(

    "logs/errors.log",

    rotation="10 MB",

    retention="10 days",

    level="ERROR",

    enqueue=True
)


# -------------------------------
# Export Logger
# -------------------------------

app_logger = logger