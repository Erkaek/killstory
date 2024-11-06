# killstory/__init__.py
"""Killstory plugin app for Alliance Auth."""

import logging
from .app_settings import KILLSTORY_LOG_LEVEL

# Configure logging pour ce module
logging.basicConfig(level=getattr(logging, KILLSTORY_LOG_LEVEL, "INFO"))

__version__ = "0.0.1"
