from django.conf.urls import url
from django.urls import path
from .views import HomePageView, homepage, HomePageListView

app_name = "home"


urlpatterns = [
    # path(r"feed", views.feed_pagination, name="feeds"),
    # url(regex=r"^feed/", view=views.feed_pagination, name='demands'),
    # url(r"^feed/$", views.feed_pagination, name="feed_pagination"),

    url(r"^$", HomePageListView.as_view(), name="home"),
    url(r"^old-home/$", homepage, name="old-home"),
    url(r"^corrected/$", HomePageView.as_view(), name="corrected3"),

]
