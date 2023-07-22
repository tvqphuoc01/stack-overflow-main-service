from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from api.jobs.scheduler import scheduler
        scheduler()
