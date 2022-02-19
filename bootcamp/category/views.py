from django.views.generic import DetailView, ListView
from .models import Category


class CategoriesListView(ListView):
    template_name = 'redico/categories.html'
    model = Category
    paginate_by = 15
    context_object_name = "categories"
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"
    # categories = []

    def get_queryset(self, **kwargs):
        queryset = super(CategoriesListView, self).get_queryset()
        return queryset.filter(category__activated=True)
        # return Category.objects.get_activated()


class CategoryDetailView(DetailView):
    template_name = 'redico/liste-article.html'
    model = Category
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # def

    def get_queryset(self, **kwargs):
        return Category.objects.get_activated()
