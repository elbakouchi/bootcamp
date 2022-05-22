from django.apps import AppConfig
import sys
from .conf import AdsConf


class CustomAdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bootcamp.customads'

    def ready(self):
        sys.modules['ads'].conf.AdsConf = AdsConf
        # print(sys.modules['ads'].conf.AdsConf.Meta.prefix)
