from django.views.generic import TemplateView
from bootcamp.category.views import CategoriesListView


class HomePageView(TemplateView, CategoriesListView):
    template_name = 'redico/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView.self).get_context_data(*args, **kwargs)
        context['categories'] = self.get_queryset(*args, **kwargs)
        return context

