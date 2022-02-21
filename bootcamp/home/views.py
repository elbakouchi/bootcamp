from django.shortcuts import render
from django.views.generic import TemplateView

from bootcamp.category.models import Category
from bootcamp.category.views import CategoriesListView


class HomePageView(CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['categories'] = super(HomePageView, self).get_queryset(**kwargs)
        return context


def homepage(request):
    categories = Category.objects.get_categories_with_demands_count()
    return render(request, 'redico/homepage.html', {'categories': categories})

