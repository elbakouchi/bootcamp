from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from .models import Category
from ..articles.models import Article
from ..demand.models import Demand


class CategoriesListView(ListView):
    template_name = 'redico/categories.html'
    model = Category
    paginate_by = 6
    context_object_name = "categories"
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # categories = []

    def get_queryset(self, **kwargs):
        # queryset = super(CategoriesListView, self).get_queryset()
        # return queryset.filter(activated=True)
        return Category.objects.get_categories_with_demands_count()


class CategoryDemandsView(SingleObjectMixin, ListView):
    template_name = 'redico/liste-article.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.get_activated())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Demand.objectz.get_category().filter(category__pk=self.object.pk)


class CategoryArticlesView(SingleObjectMixin, ListView):
    template_name = 'redico/liste-article.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.get_activated())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Article.objects.get_category().filter(demand__category__pk=self.object.pk)


class CategoryDetailView(DetailView):
    template_name = 'redico/liste-article.html'
    model = Category
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # def

    def get_queryset(self, **kwargs):
        return Category.objects.all()
