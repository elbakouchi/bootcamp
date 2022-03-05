from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from bootcamp.helpers import ajax_required, AuthorRequiredMixin
from django.views.decorators.http import require_http_methods

from bootcamp.articles.models import Article
from bootcamp.articles.forms import ArticleForm


class ArticlesListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published articles list."""

    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["popular_tags"] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()


class DraftsListView(ArticlesListView):
    """Overriding the original implementation to call the drafts articles
    list."""

    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()


class CreateArticleView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""

    model = Article
    message = _("Your article has been created.")
    form_class = ArticleForm
    template_name = "articles/article_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:list")


class EditArticleView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing articles."""

    model = Article
    message = _("Your article has been updated.")
    form_class = ArticleForm
    template_name = "articles/article_update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:list")


class DetailArticleView(DetailView):
    """Basic DetailView implementation to call an individual article."""
    template_name = "redico/article-single.html"
    context_object_name = 'article'
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super(DetailArticleView, self).get_queryset()
        return queryset.get_category()


# @login_required
# @ajax_required
@require_http_methods(["GET"])
def get_category_articles(request, pk, page, page_size):
    """Returns a paginated list of articles with the given category id."""
    category_id = pk if pk is not None else request.GET["category"]

    articles, paginator = get_paginated_articles(category_id, page, page_size)

    articles_html = render_to_string("redico/articles/paginated_articles.html", {"articles": paginator.get_page(page)})

    pagination_html = render_to_string(
        "redico/articles/articles_pagination.html", {"current": paginator.page(page),
                                                     "page_range": paginator.page_range}
    )
    return JsonResponse({"category_id": category_id,
                         "articles_html": articles_html,
                         "pagination_html": pagination_html
                         })


def get_paginated_articles(category_id, page, page_size):
    articles = Article.objects.get_category().filter(demand__category__pk=category_id)
    paginator = Paginator(articles, page_size)
    return articles, paginator


def paginate(request, pk, page):
    category_id = pk if pk is not None else request.GET["category"]
    page = request.GET.get('page', None)
    pk = request.GET.get('pk', None)
    starting_number = (page - 1) * 6
    ending_number = page * 6

    result = Article.objects.get_category().filter(demand__category__pk=category_id)[starting_number:ending_number]
    data = {result}

    return JsonResponse(data)
