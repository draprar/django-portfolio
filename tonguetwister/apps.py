from django.apps import AppConfig


class TongueTwisterConfig(AppConfig):
    name = 'tonguetwister'

    def ready(self):
        # Ensure signal receivers are registered at app startup.
        from . import signals  # noqa: F401
