from django.views.generic import TemplateView
from bootcamp.category.views import CategoriesListView


class HomePageView(CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListView, self).get_context_data(*args, **kwargs)
        context['categories'] = super(CategoriesListView, self).get_queryset(**kwargs)
        return context

