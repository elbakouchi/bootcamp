import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User

from PIL import Image
from django import forms

from ..demand.models import Demand


class CustomUserForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = '__all__'


class UserDetailView(LoginRequiredMixin, ModelFormMixin, DetailView):
    model = User
    form_class = CustomUserForm
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'redico/profile.html'
    # fields = ['first_name', 'last_name', 'phone', 'email', 'bio', 'picture']
    success_url = "/users/{username}/"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        try:
            demands = Demand.objects.profile(self.request.user.pk, self.request.GET.o)
        except:
            demands = Demand.objects.profile(self.request.user.pk, '')
        context["demands_count"] = demands.count()

        page = self.request.GET.get("page", 1)
        paginator = Paginator(demands, 5)

        try:
            paginated_demands = paginator.page(page)
        except PageNotAnInteger:
            paginated_demands = paginator.page(1)
        except EmptyPage:
            paginated_demands = paginator.page(paginator.num_pages)
        context["demands"] = paginated_demands
        return context

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'redico/profile.html'
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

    def form_valid(self, form):
        uploaded = upload_picture(self.request)
        if uploaded:
            filename = save_uploaded_picture(self.request)
            self.object.picture.name = filename
            self.object.save()
        return super(UserUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form)

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        try:
            demands = Demand.objects.profile(self.request.user.pk, self.request.GET.o)
        except Exception as e:
            demands = Demand.objects.profile(self.request.user.pk, '')
        context["demands_count"] = demands.count()
        page = self.request.GET.get("page", 1)
        paginator = Paginator(demands, 5)

        try:
            paginated_demands = paginator.page(page)
        except PageNotAnInteger:
            paginated_demands = paginator.page(1)
        except EmptyPage:
            paginated_demands = paginator.page(paginator.num_pages)
        context["demands"] = paginated_demands
        return context


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get("upload_picture") == "uploaded":
            uploaded_picture = True

    except Exception:  # pragma: no cover
        pass

    return render(
        request, "users/user_picture.html", {"uploaded_picture": uploaded_picture}
    )


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + "/profile_pics/"
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)

        f = request.FILES["picture"]
        filename = profile_pictures + request.user.username + "_tmp.jpg"
        with open(filename, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        # return redirect("/users/picture/?upload_picture=uploaded")
        return True
    except Exception as e:
        print(e)
        return False
        # return redirect("/users/picture/")


#@login_required
def save_uploaded_picture(request):
    try:
        x = float(request.POST.get("x"))
        y = float(request.POST.get("y"))
        w = float(request.POST.get("width"))
        h = float(request.POST.get("height"))
        tmp_filename = (
                django_settings.MEDIA_ROOT
                + "/profile_pics/"
                + request.user.username
                + "_tmp.jpg"
        )
        filename = (
                django_settings.MEDIA_ROOT
                + "/profile_pics/"
                + request.user.username
                + ".jpg"
        )
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        return f"/profile_pics/{request.user.username}.jpg"
    except Exception as e:
        print(e)
        pass

    #return redirect("/users/picture/")
