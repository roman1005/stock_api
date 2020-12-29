from django.apps import AppConfig


class StockApisBeConfig(AppConfig):
    name = 'stock_apis_BE'

    def ready(self):

        from stock_apis_BE import Articles_Updater

        Articles_Updater.start()