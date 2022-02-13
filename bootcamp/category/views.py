from django.shortcuts import render
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from .models import Category

class CategoriesListView(ListView):
    model = Category
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"
     def get_queryset(self, **kwargs):
        return Category.objects.get_activated()

class CategoryDetailView(DetailView):
    model = Category
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"    
