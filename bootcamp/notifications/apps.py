from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"	
    name = "bootcamp.notifications"
    verbose_name = _("Notifications")
