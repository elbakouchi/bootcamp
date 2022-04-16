from django.http import JsonResponse
from allauth.account.views import SignupView, _ajax_response, LogoutView

from bootcamp.articles.models import Article
from bootcamp.demand.models import Demand
from bootcamp.users.views import UserUpdateView, UserDetailView
from allauth.account.forms import UserForm


class ProfileView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        user_form = UserForm()
        demands = Demand.objects.filter(user=self.object.pk).order_by('pk', 'timestamp')
        revisions = Article.objects.filter(user=self.object.pk).order_by('pk', 'timestamp')
        if revisions.count():
            context["last_revision"] = revisions.last().content
        context["demands"] = demands
        context["revisions"] = revisions
        context["user_form"] = user_form
        return context


class AjaxLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            response = self.form_valid(form)
            return _ajax_response(
                self.request, response, form=form, data=self._get_ajax_data_if())
        else:
            return JsonResponse({'errors': form.errors})
