from django.views.generic import TemplateView
from bootcamp.category.views import CategoriesListView


class HomePageView(TemplateView, CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.get_queryset(*args, **kwargs)
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return context

