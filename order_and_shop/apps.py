from django.apps import AppConfig


class OrderAndShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_and_shop'

    def ready(self):
        import order_and_shop.signals
