from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    #for signals.py
    def ready(self):
        import accounts.signals
