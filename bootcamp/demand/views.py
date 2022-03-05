from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _

from bootcamp.demand.forms import DemandForm
from bootcamp.demand.models import Demand


class CreateDemandView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""

    model = Demand
    message = _("Your article has been created.")
    form_class = DemandForm
    template_name = "redico/new-article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
