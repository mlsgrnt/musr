from django.apps import AppConfig


class MusrConfig(AppConfig):
    name = "musr"

    def ready(self):
        import musr.signals
