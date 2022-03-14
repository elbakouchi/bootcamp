from django.conf.urls import url
from bootcamp.demand.views import CreateDemandView, DetailDemandView, PaginatedDemandsFeed

app_name = 'demands'

urlpatterns = [
    url(r"^nouveau-text/$", CreateDemandView.as_view(), name="write_new"),
    # url(regex=r"^$", view=CategoriesListView.as_view(), name='list'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDetailView.as_view(), name='detail'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryArticlesView.as_view(), name='articles')
    url(r"^(?P<slug>[-\w]+)/$", DetailDemandView.as_view(), name="demand"),
    url(r"^feed/$", PaginatedDemandsFeed.as_view(), name="demands_feed")

]
