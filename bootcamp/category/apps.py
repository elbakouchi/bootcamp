from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "bootcamp.gategory"
    verbose_name = _("Categories")