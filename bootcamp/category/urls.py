from django.conf.urls import url
from bootcamp.category.views import CategoriesListView, CategoryArticlesView, CategoryDemandsView

app_name = 'categories'

urlpatterns = [
    url(regex=r"^$", view=CategoriesListView.as_view(), name='list'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDetailView.as_view(), name='detail'),
    # url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryArticlesView.as_view(), name='articles'),
    url(regex=r"^(?P<slug>[\w.@+-]+)/$", view=CategoryDemandsView.as_view(), name='demands')
]
