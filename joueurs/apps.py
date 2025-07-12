from django.apps import AppConfig

class JoueursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'joueurs'

    def ready(self):
        import joueurs.signals
