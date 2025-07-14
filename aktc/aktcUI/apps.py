from django.apps import AppConfig
# from django.contrib.admin.apps import AdminConfig


# class AktcAdminConfig(AdminConfig):
#     default_site = 'aktcUI.admin.AKTCAdminSite'


class AktcuiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aktcUI'

    def ready(self):
        import aktcUI.signals
