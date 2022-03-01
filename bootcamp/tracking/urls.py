from django.conf.urls import url

from bootcamp.tracking.views import dashboard

urlpatterns = [
    url(r'^$', dashboard, name='tracking-dashboard'),
]
