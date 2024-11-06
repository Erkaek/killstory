# killstory/__init__.py

"""Killstory plugin app for Alliance Auth."""

import logging
from django.apps import apps
from .app_settings import KILLSTORY_LOG_LEVEL

# Set up logging for this module based on the specified log level
logging.basicConfig(level=getattr(logging, KILLSTORY_LOG_LEVEL, "INFO"))

# Set the default application configuration
default_app_config = "killstory.apps.KillstoryConfig"

# Import tasks only when apps are ready
def ready():
    if apps.ready:
        from . import tasks  # noqa: F401

__version__ = "0.0.1"
