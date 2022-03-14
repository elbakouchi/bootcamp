from django.conf.urls import url
from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    # path(r"feed", views.feed_pagination, name="feeds"),
    # url(regex=r"^feed/", view=views.feed_pagination, name='demands'),
    # url(r"^feed/$", views.feed_pagination, name="feed_pagination"),
    url(r"^$",  views.homepage, name="home"),

]