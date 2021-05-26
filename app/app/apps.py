from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = "app"

    def ready(self):
        from polaris.integrations import register_integrations
        from .integrations import GrcRailsIntegration, GrcDepositIntegration, GrcWithdrawalIntegration, Utility

        register_integrations(
            deposit=GrcDepositIntegration(),
            withdrawal=GrcWithdrawalIntegration(),
            rails=GrcRailsIntegration(),
            fee=Utility.calculate_fee
        )