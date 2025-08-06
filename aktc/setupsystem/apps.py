from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class SetupsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'setupsystem'
    verbose_name = _("Schedule Setup System")

    def ready(self):
        import setupsystem.signals

