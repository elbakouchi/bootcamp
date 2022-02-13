from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MessagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"	
    name = "bootcamp.messager"
    verbose_name = _("Messager")
