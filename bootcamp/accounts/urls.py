from django.conf.urls import url
from .views import *

app_name = "accounts"
urlpatterns = [
    url(r"^(?P<username>[\w.@+-]+)/$", ProfileView.as_view(), name="profile"),
]