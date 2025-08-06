from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FeedbacksystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedbacksystem'
    verbose_name = _("Passenger Feedback System")
