from django.apps import AppConfig
import seqlog
from django.conf import settings

class MyAppConfig(AppConfig):
    name = "server"

    def ready(self):
        from polaris.integrations import register_integrations
        from .integrations import GrcRailsIntegration, GrcDepositIntegration, GrcWithdrawalIntegration

        register_integrations(
            deposit=GrcDepositIntegration(),
            withdrawal=GrcWithdrawalIntegration(),
            rails=GrcRailsIntegration()
        )
