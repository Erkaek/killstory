# killstory/__init__.py

"""Killstory plugin app for Alliance Auth."""

import logging

# Import the settings to get the logging level
try:
    from .app_settings import KILLSTORY_LOG_LEVEL
except ImportError:
    KILLSTORY_LOG_LEVEL = "INFO"  # Default to INFO if setting is missing

# Set up logging for this module based on the specified log level
logging.basicConfig(level=getattr(logging, KILLSTORY_LOG_LEVEL, logging.INFO))

# Import tasks to ensure Celery registers them
from . import tasks  # noqa: F401

# Set the default application configuration
default_app_config = "killstory.apps.KillstoryConfig"

__version__ = "0.0.1"
