"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from bootcamp.notifications.consumers import NotificationsConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()
# application = get_default_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "https": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        url(r"^notifications/$", NotificationsConsumer),
                    ]
                )
            )
        )
})

