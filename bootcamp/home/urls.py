from django.conf.urls import url
from bootcamp.home.views import HomePageView, homepage


app_name = "home"
urlpatterns = [
    url(r"^$", 'bootcamp.home.views.homepage', name="home"),
]