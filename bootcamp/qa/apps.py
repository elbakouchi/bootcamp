from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"	
    name = "bootcamp.qa"
    verbose_name = _("Q&A")
