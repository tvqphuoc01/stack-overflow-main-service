from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from api.jobs.scheduler import scheduler
        from firebase_admin import credentials
        import firebase_admin
        scheduler()

        creds = credentials.Certificate(
            'api/utils/stackoverflow-393008-firebase-adminsdk-vqhrr-4c51a47f2c.json')
        default_app = firebase_admin.initialize_app(creds)
