from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "bootcamp.category"
    verbose_name = _("Categories")