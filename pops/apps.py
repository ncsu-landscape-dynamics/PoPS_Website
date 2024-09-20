from django.apps import AppConfig


class PopsConfig(AppConfig):
    name = "pops"

    def ready(self):
        from pops import receivers