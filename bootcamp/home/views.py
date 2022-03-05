from django.db.models import Count
from django.shortcuts import render
from django.contrib.postgres.aggregates import StringAgg
# from django.views.generic import TemplateView

from bootcamp.category.models import Category
from bootcamp.category.views import CategoriesListView
from bootcamp.demand.models import Demand


class HomePageView(CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['categories'] = super(HomePageView, self).get_queryset(**kwargs)
        return context


def homepage(request):
    demands = \
        Demand.objects.filter(status="P").annotate(categoryName=StringAgg('category__name', delimiter=','))
    categories = Category.objects.filter(activated=True).annotate(posts_count=Count('demand_category'))
    return render(request, 'redico/homepage.html', {'categories': categories, 'demands': demands})

