from django.http import JsonResponse
from allauth.account.views import SignupView, _ajax_response, LogoutView
from django.shortcuts import redirect
from bootcamp.articles.models import Article
from bootcamp.demand.models import Demand
from bootcamp.users.views import UserUpdateView, UserDetailView
from allauth.account.forms import UserForm, SignupForm
from django.forms.fields import BooleanField
from allauth.account.views import SignupView


class CustomSignupForm(SignupForm):
    terms = BooleanField()


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


class ProfileView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        user_form = UserForm()
        demands = Demand.objectz.filter(user=self.object.pk).order_by('pk', 'timestamp')
        revisions = Article.objects.filter(user=self.object.pk).order_by('pk', 'timestamp')
        if revisions.count():
            context["last_revision"] = revisions.last().content
        context["demands"] = demands
        context["revisions"] = revisions
        context["user_form"] = user_form
        return context


class AjaxLogoutView(LogoutView):
    def get(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated:
            self.logout()
        return JsonResponse({'url': url})
