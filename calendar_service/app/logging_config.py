import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.setLevel(logging.INFO)
uvicorn_access_logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(settings.LOG_DIR / "app.log", maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
uvicorn_logger.addHandler(console_handler)
uvicorn_logger.addHandler(file_handler)
uvicorn_access_logger.addHandler(console_handler)
uvicorn_access_logger.addHandler(file_handler)
