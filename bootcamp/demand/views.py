from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from bootcamp.category.models import Category
from bootcamp.articles.forms import SuggestedRevisionForm
from bootcamp.articles.models import Article
from bootcamp.custom import AjaxListView
from bootcamp.demand.forms import DemandForm
from bootcamp.demand.models import Demand
from bootcamp.notifications.models import Notification
from bootcamp.helpers import AuthorRequiredMixin
from django.shortcuts import redirect


class DetailDemandView(DetailView):
    """Basic DetailView implementation to call an individual article."""
    template_name = "redico/article-single3.html"
    context_object_name = 'demand'
    model = Demand

    def get_context_data(self, **kwargs):
        context = super(DetailDemandView, self).get_context_data()
        suggest_form = SuggestedRevisionForm()
        # revisions = Article.objects.filter(demand_id=OuterRef("id"),).order_by("-timestamp")
        revisions = Article.objects.filter(demand=self.object.pk).order_by('-pk')
        # if revisions.count():
        #    context["last_revision"] = revisions.last().content
        context["revisions"] = revisions
        context["suggest_form"] = suggest_form
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(DetailDemandView, self).get_queryset()
        return queryset.get_annotated_demand()


class CreateDemandView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""

    model = Demand
    message = """Votre texte a bien été envoyé, vous recevrez une notification dès qu’une nouvelle correction sera suggérée.\
        <br><a href="/">En attendant, vous pouvez consulter ici des exemples de textes corrigés</a>"""
    form_class = DemandForm
    template_name = "redico/new-article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("demands:edit_demand", kwargs={'pk': self.object.pk})


class CategoryDemandsList(SingleObjectMixin, ListView):
    paginate_by = 5
    paginate_orphans = 1
    template_name = "redico/category-demands.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.get_activated())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Demand.objectz.get_category_demands(self.object.slug)


class DemandsList(ListView):
    model = Demand
    paginate_by = 5
    paginate_orphans = 1
    template_name = "redico/unfulfilled-demands-paginated.html"

    def get_queryset(self):
        # return Demand.objectz.get_without_revisions().filter(revision_count__lt=1)
        return Demand.objectz.get_published_unverified_demands()


class PaginatedDemandsFeed(AjaxListView):
    model = Demand
    paginate_by = 5
    paginate_orphans = 1
    page_template = "redico/snippets/demand-list-item-2.html"
    context_object_name = "demands"

    def get_queryset(self):
        # return Demand.objectz.get_without_revisions().filter(revision_count__lt=1)
        return Demand.objectz.get_published_unverified_demands()


class PaginatedDemandsHomeFeed(AjaxListView):
    model = Demand
    paginate_by = 5
    page_template = "redico/snippets/demand-list-item-2.html"
    context_object_name = "demands"

    def get_queryset(self):
        return Demand.objectz.get_category()


class EditDemandView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing demands."""

    model = Demand
    message = """Votre texte a été mis a jour avec succès."""
    form_class = DemandForm
    template_name = "redico/update-article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("home:home")


class CorrectedDemandsView(ListView):
    model = Demand
    paginate_by = 10
    paginate_orphans = 1
    context_object_name = "demands"
    template_name = 'redico/corrected-demands-paginated.html'
    queryset = Demand.objectz.corrected_demands()


def demand_redirect(request, pk):
    demand = Demand.objectz.get(pk=pk)
    if demand:
        Notification.objects.mark_as_read(recipient=request.user, action_obj=pk)
        return redirect(reverse('demands:demand', args=[demand.slug]))
