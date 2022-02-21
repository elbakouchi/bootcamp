from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from bootcamp.articles.models import Article
from bootcamp.category.models import Category
from bootcamp.category.views import CategoriesListView


class HomePageView(CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['categories'] = super(HomePageView, self).get_queryset(**kwargs)
        return context


def homepage(request):
    articles = Article.objects.filter(published=True)
    categories = Category.objects.filter(activated=True).annotate(posts_count=Count('taxonomy_category'))
    return render(request, 'redico/homepage.html', {'categories': categories, 'articles':articles})

