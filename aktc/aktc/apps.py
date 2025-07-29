from django.contrib.admin.apps import AdminConfig


class AktcAdminConfig(AdminConfig):
    default_site = 'aktc.admin.AktcAdminSite'
