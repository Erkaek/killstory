# killstory/app_settings.py

"""App settings for the Killstory plugin."""

from django.conf import settings

# Define default settings with getattr, allowing them to be overridden in the main project settings.
KILLSTORY_API_LIST_ENDPOINT = getattr(settings, "KILLSTORY_API_LIST_ENDPOINT", "https://killstory.soeo.fr/{}.json")
KILLSTORY_API_DETAIL_ENDPOINT = getattr(settings, "KILLSTORY_API_DETAIL_ENDPOINT", "https://esi.evetech.net/latest/killmails/{}/{}")

# Optional settings with reasonable defaults
KILLSTORY_BATCH_SIZE = getattr(settings, "KILLSTORY_BATCH_SIZE", 100)
KILLSTORY_RETRY_LIMIT = getattr(settings, "KILLSTORY_RETRY_LIMIT", 5)
KILLSTORY_LOG_LEVEL = getattr(settings, "KILLSTORY_LOG_LEVEL", "INFO")  # Can be "DEBUG", "INFO", "WARNING", etc.
