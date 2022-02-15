from django.views.generic import DetailView, ListView
from .models import Category


class CategoriesListView(ListView):
    template_name = 'redico/categories.html'
    model = Category
    paginate_by = 15
    # context_object_name = "categories"
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"
    # categories = []

    def get_queryset(self, **kwargs):
        queryset = kwargs.pop('categories', None)
        if queryset is None:
            self.object_list = Category.objects.get_activated()
        return queryset


class CategoryDetailView(DetailView):
    model = Category
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"
