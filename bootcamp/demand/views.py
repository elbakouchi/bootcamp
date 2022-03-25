from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from bootcamp.articles.forms import SuggestedRevisionForm
from bootcamp.articles.models import Article
from bootcamp.custom import AjaxListView
from bootcamp.demand.forms import DemandForm
from bootcamp.demand.models import Demand


class DetailDemandView(DetailView):
    """Basic DetailView implementation to call an individual article."""
    template_name = "redico/article-single3.html"
    context_object_name = 'demand'
    model = Demand

    def get_context_data(self, **kwargs):
        context = super(DetailDemandView, self).get_context_data()
        suggest_form = SuggestedRevisionForm()
        context["revisions"] = Article.objects.filter(demand=self.object.pk, verified=True)
        context["suggest_form"] = suggest_form
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(DetailDemandView, self).get_queryset()
        return queryset.get_category()


class CreateDemandView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""

    model = Demand
    message = _("Your demand has been created.")
    form_class = DemandForm
    template_name = "redico/new-article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("home:home")


class DemandsList(ListView):
    model = Demand
    paginate_by = 1
    template_name = "redico/unfulfilled-demands.html"

    def get_queryset(self):
        return Demand.objects.get_without_revisions()


class PaginatedDemandsFeed(AjaxListView):
    model = Demand
    paginate_by = 5
    page_template = "redico/snippets/demand-list-item-2.html"
    context_object_name = "demands"

    def get_queryset(self):
        return Demand.objects.get_category()
