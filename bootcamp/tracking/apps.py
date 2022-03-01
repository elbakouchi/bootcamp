from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save


class TrackingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bootcamp.tracking"
    verbose_name = _("Tracking")
    '''
        def ready(self, tracking=None):
        from bootcamp.tracking import handlers
        from bootcamp.tracking.models import Visitor
        user_logged_out.connect(handlers.track_ended_session)
        post_save.connect(handlers.post_save_cache, sender=Visitor)
    '''
