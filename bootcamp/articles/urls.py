from django.conf.urls import url

from bootcamp.articles.views import (
    ArticlesListView,
    DraftsListView,
    CreateArticleView,
    EditArticleView,
    DetailArticleView,
    get_category_articles
)

app_name = "articles"
urlpatterns = [
    url(r"^$", ArticlesListView.as_view(), name="list"),
    url(r"^write-new-article/$", CreateArticleView.as_view(), name="write_new"),
    url(r"^drafts/$", DraftsListView.as_view(), name="drafts"),
    url(r"^edit/(?P<pk>\d+)/$", EditArticleView.as_view(), name="edit_article"),
    url(r"^(?P<pk>\d+)/$", DetailArticleView.as_view(), name="article_pk"),
    url(r"^(?P<slug>[-\w]+)/$", DetailArticleView.as_view(), name="article"),
    url(r"^get-category-articles/(?P<pk>\d+)/(?P<page>\d+)/(?P<page_size>\d+)$", get_category_articles,
        name="get_category_paginated_articles"),
]
