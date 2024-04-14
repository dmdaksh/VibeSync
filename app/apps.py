from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        import os

        if not os.path.exists("app/static/app/audios"):
            os.makedirs("app/static/app/audios")
