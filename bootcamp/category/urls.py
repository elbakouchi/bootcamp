from django.conf.urls import url
from .views import CategoriesListView, CategoryDetailView

app_name = "categories"
urlpatterns = [
    url(regex=r"^$", view=CategoriesListView.as_view(), name="list"),
    #url(regex=r"^~redirect/$", view=UserRedirectView.as_view(), name="redirect"),
    #url(regex=r"^~update/$", view=UserUpdateView.as_view(), name="update"),
    url(
        regex=r"^(?P<slug>[\w.@+-]+)/$",
        view=CategoryDetailView.as_view(),
        name="detail",
    ),
]