from django.conf.urls import url
from bootcamp.home.views import HomePageView


app_name = "home"
urlpatterns = [
    url(r"^$", HomePageView.as_view(), name="home"),
]