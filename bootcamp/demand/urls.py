from django.conf.urls import url
from bootcamp.demand.views import CreateDemandView, DetailDemandView, \
    PaginatedDemandsFeed, DemandsList, PaginatedDemandsHomeFeed, \
    EditDemandView, demand_redirect
app_name = 'demands'


urlpatterns = [
    url(r"^home-feed/$", PaginatedDemandsHomeFeed.as_view(), name="home_demands_feed"),
    url(r"^feed/$", PaginatedDemandsFeed.as_view(), name="demands_feed"),
    url("^en-attente-de-reponse/$", DemandsList.as_view(), name="unfulfilled"),
    url(r"^nouveau-text/$", CreateDemandView.as_view(), name="write_new"),
    # url(regex=r"^$", view=CategoriesListView.as_view(), name='list'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDetailView.as_view(), name='detail'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryArticlesView.as_view(), name='articles')
    url(r"^(?P<slug>[-\w]+)/$", DetailDemandView.as_view(), name="demand"),
    url(r"^r/(?P<pk>\d+)/$", demand_redirect, name="redirect_demand"),
    url(r"^editer/(?P<pk>\d+)/$", EditDemandView.as_view(), name="edit_demand")
]


