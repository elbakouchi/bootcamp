from django.conf.urls import url
from bootcamp.category.views import CategoriesListView, CategoryDetailView

app_name = 'categories'

urlpatterns = [
    url(regex=r"^$", view=CategoriesListView.as_view(), name='list'),
    url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDetailView.as_view(), name='detail')
]
