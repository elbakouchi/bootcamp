from django.conf.urls import url

from . import views

app_name = "categories"
urlpatterns = [
    url(regex=r"^$", view=views.CategoriesListView.as_view(), name="list"),
    #url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    #url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    url(
        regex=r"^(?P<slug>[\w.@+-]+)/$",
        view=views.CategoryDetailView.as_view(),
        name="detail",
    ),
]