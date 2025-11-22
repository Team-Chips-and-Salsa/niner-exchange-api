from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # This import runs the initialization code in firebase_config.py
        import core.firebase_config
        import core.signals
