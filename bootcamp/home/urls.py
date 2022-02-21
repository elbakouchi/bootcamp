from django.conf.urls import url
from bootcamp.home import views


app_name = "home"
urlpatterns = [
    url(r"^$",  views.homepage, name="home"),
]