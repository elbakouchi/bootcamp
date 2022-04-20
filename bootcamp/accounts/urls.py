from django.conf.urls import url
from .views import *

app_name = "accounts"
urlpatterns = [
    url(r"^destroy/$", AjaxLogoutView.as_view(), name="destroy"),
    url(r"^(?P<username>[\w.@+-]+)/$", ProfileView.as_view(), name="profile"),

]
