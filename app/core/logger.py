import logging
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler(
    "app/core/logs/service.log", maxBytes=5 * 1024 * 1024, backupCount=5
)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)