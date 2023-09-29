from django.apps import AppConfig


class PaymentsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments_app'

    verbose_name = 'PAYMENTS'

    # signal for subaccount creation for paystack 
    def ready(self) -> None:
        import payments_app.payment_signals