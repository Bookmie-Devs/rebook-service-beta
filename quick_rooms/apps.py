from django.apps import AppConfig


class QuickRoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quick_rooms'

    def ready(self) -> None:
        import quick_rooms.signals

