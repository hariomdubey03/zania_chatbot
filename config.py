import os
from pathlib import Path
import logging
from logging import config
from dotenv import load_dotenv
import os

# Logging Config
log_config = {
    "version": 1,
    "root": {"handlers": ["console", "file"], "level": "DEBUG"},
    "handlers": {
        "console": {
            "formatter": "stream_formatter",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file": {
            "filename": "logs/zania_chatbot_service.log",
            "formatter": "file_formatter",
            "class": "logging.FileHandler",
            "level": "INFO",
        },
    },
    "formatters": {
        "stream_formatter": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        },
        "file_formatter": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        },
    },
}
config.dictConfig(log_config)

logger = logging.getLogger("CONFIG")

BASE_DIR = Path(__file__).resolve().parent

env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)


# Check & Fetch ENV Variables
def get_env_value(key_):
    if os.getenv(key_):
        return os.environ[key_]
    else:
        raise KeyError(
            f'KEY "{key_}" NOT FOUND IN THE ENVIRONMENT FILE. PLEASE ADD TO PROCEED'
        )


TIMEZONE = get_env_value("TIMEZONE")
REDIS_URL = get_env_value("REDIS_URL")
