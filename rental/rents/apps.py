from django.apps import AppConfig


class RentsConfig(AppConfig):
    name = 'rental.rents'
    verbose_name = "Rents"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
