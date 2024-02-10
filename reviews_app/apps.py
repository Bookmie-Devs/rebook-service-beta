from django.apps import AppConfig


class ReviewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews_app'

    def ready(self):
        import reviews_app.news_letter
