from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DemandsConfig(AppConfig):
    name = "bootcamp.demand"
    verbose_name = _("Demands")
