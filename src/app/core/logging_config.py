import logging
from logging.config import dictConfig
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": LOG_LEVEL,
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "app.log",
            "mode": "a",
            "level": LOG_LEVEL,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },
}

dictConfig(logging_config)

logger = logging.getLogger("app")
