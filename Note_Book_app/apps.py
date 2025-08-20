from django.apps import AppConfig


class NoteBookAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Note_Book_app'
    
    def ready(self):
        import Note_Book_app.signals