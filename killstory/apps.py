from django.apps import AppConfig


class KillstoryConfig(AppConfig):
    name = "killstory"  # This should match the actual module path.
    label = "killstory"  # This will be the internal label Django uses.
    verbose_name = (
        "Killstory"  # This will be the human-readable name in the admin interface.
    )
