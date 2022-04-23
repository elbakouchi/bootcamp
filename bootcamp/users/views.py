from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User
from django.db.models import Count, F
from itertools import chain
from ..articles.models import Article
from ..demand.models import Demand


class UserDetailView(LoginRequiredMixin, ModelFormMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'redico/profile.html'
    fields = ['first_name', 'last_name', 'phone', 'email', 'bio', 'picture']
    success_url = "/users/{username}/"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        demands = Demand.objects.filter(user=self.object.pk).order_by('pk', 'timestamp').annotate(service_name=F('service__name'),
            revision_count=Count('revision__id', None))
        context["demands_count"] = demands.count()

        page = self.request.GET.get("page", 1)
        paginator = Paginator(demands, 5)

        try:
            paginated_demands = paginator.page(page)
        except PageNotAnInteger:
            paginated_demands = paginator.page(1)
        except EmptyPage:
            paginated_demands = paginator.page(paginator.num_pages)

        revisions = Article.objects.filter(user=self.object.pk).order_by('pk', 'timestamp')
        context["revisions_count"] = revisions.count()
        paginator2 = Paginator(revisions, 5)

        try:
            paginated_revisions = paginator2.page(page)
        except PageNotAnInteger:
            paginated_revisions = paginator2.page(1)
        except EmptyPage:
            paginated_revisions = paginator2.page(paginator2.num_pages)

        context["revisions"] = paginated_revisions
        context["demands"] = paginated_demands
        '''
        combined = chain(demands, revisions)
        paginator3 = Paginator(combined, 5)

        try:
            paginated_combined = paginator3.page(page)
        except PageNotAnInteger:
            paginated_combined = paginator3.page(1)
        except EmptyPage:
            paginated_combined = paginator3.page(paginator.num_pages)

        context["combined"] = paginated_combined
        '''
        return context

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "picture",
        "job_title",
        "location",
        "personal_url",
        "facebook_account",
        "twitter_account",
        "github_account",
        "linkedin_account",
        "short_bio",
        "bio",
    ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
