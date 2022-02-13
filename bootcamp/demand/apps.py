from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DemandsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bootcamp.demand"
    verbose_name = _("Demands")
