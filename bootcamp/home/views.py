from django.views.generic import TemplateView
from bootcamp.category.views import CategoriesListView


class HomePageView(TemplateView, CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = super().get_queryset(**kwargs)
        return context

