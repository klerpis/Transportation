from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
# from django.contrib.admin.apps import AdminConfig


# class AktcAdminConfig(AdminConfig):
#     default_site = 'aktcUI.admin.AKTCAdminSite'


class AktcuiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aktcUI'
    verbose_name = _("AKTC Control Interface")


    def ready(self):
        import aktcUI.signals
