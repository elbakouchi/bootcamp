from django.conf.urls import url
from bootcamp.demand.views import CreateDemandView

app_name = 'demands'

urlpatterns = [
    # url(regex=r"^$", view=CategoriesListView.as_view(), name='list'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDetailView.as_view(), name='detail'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryArticlesView.as_view(), name='articles')
    url(r"^nouveau-text/$", CreateDemandView.as_view(), name="write_new")
]
