import os
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from contact_form.views import ContactFormView
from contact_form.forms import StringKeyedDict
from django.template import loader
from django.contrib import messages

from .models import User
from .forms import CustomContactForm, CustomServicesForm
from PIL import Image
from django import forms

from ..demand.models import Demand


class CustomServicesFormView(ContactFormView):
    form_class = CustomServicesForm
    recipient_list = None
    success_url = reverse_lazy("contact_form_sent")
    template_name = "redico/services.html"

    '''
    def form_valid(self, form) -> HttpResponse:
        #form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(CustomServicesFormView, self).get_context_data(**kwargs)
        #context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context
    def get_form_kwargs(self) -> StringKeyedDict:
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        # We may also have been given a recipient list when
        # instantiated.
        if self.recipient_list is not None:
            kwargs.update({"recipient_list": self.recipient_list})
        return kwargs
    '''
class CustomContactFormView(ContactFormView):
    form_class = CustomContactForm
    recipient_list = None
    success_url = reverse_lazy("contact_form_sent")
    template_name = "redico/contact.html"

    def form_valid(self, form) -> HttpResponse:
        # recaptcha_response = self.request.POST.get('g-recaptcha-response')
        # data = {
        #     'secret': settings.RECAPTCHA_PRIVATE_KEY,
        #    'response': recaptcha_response
        # }
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        # result = r.json()

        # print(result)

        ''' if reCAPTCHA returns True '''
        # if result['success']:
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CustomContactFormView, self).get_context_data(**kwargs)
        context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def get_form_kwargs(self) -> StringKeyedDict:
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        # We may also have been given a recipient list when
        # instantiated.
        if self.recipient_list is not None:
            kwargs.update({"recipient_list": self.recipient_list})
        return kwargs


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
    template_name = 'redico/profile4.html'
    # fields = ['first_name', 'last_name', 'phone', 'email', 'bio', 'picture']
    success_url = "/users/{username}/"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        try:
            demands = Demand.objectz.profile(self.request.user.pk, self.request.GET.o)
        except:
            demands = Demand.objectz.profile(self.request.user.pk, '')
        context["demands_count"] = demands.count()

        page = self.request.GET.get("page", 1)
        paginator = Paginator(demands, 5, 2)

        try:
            paginated_demands = paginator.page(page)
        except PageNotAnInteger:
            paginated_demands = paginator.page(1)
        except EmptyPage:
            paginated_demands = paginator.page(paginator.num_pages)
        context["demands"] = paginated_demands
        context['passwform'] = PasswordChangeForm(self.request.user, self.request.POST )
        return context

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


from django.http import HttpResponse


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    form_class = PasswordChangeForm
    template_name = 'redico/profile4.html'
    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)
    model = User
    def get_success_url(self):
        return reverse("home:home")
        """response = render(self.request, 'redico/profile4.html', {
           'passwform':  PasswordChangeForm(self.request.user), 'demands': self.get_demands(), 'form': CustomUserForm(self.request.user)
        })    
        return HttpResponse(response, content_type='text/html')"""    

    def get(self, request, *args, **kwargs):
        response = render(request, 'redico/profile4.html', {
           'passwform':  PasswordChangeForm(self.request.user), 'demands': self.get_demands(), 'form': CustomUserForm()
        })    
        return HttpResponse(response, content_type='text/html')     
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Mot de passe changé avec succès!')
            #return reverse("users:detail", kwargs={"username": self.request.user.username})
        else:
            messages.error(request, 'Veuillez corriger!')
        response = render(request, 'redico/profile4.html', {
            'passwform':  form, 'demands': self.get_demands(), 'form': CustomUserForm()
         })    
        return HttpResponse(response, content_type='text/html')  

    def get_demands(self, **kwargs):
        try:
            demands = Demand.objectz.profile(self.request.user.pk, self.request.GET.o)
        except Exception as e:
            demands = Demand.objectz.profile(self.request.user.pk, '')
        page = self.request.GET.get("page", 1)
        paginator = Paginator(demands, 5)

        try:
            paginated_demands = paginator.page(page)
        except PageNotAnInteger:
            paginated_demands = paginator.page(1)
        except EmptyPage:
            paginated_demands = paginator.page(paginator.num_pages)
        #context["demands"] = paginated_demands
        #context['form'] = CustomUserForm(self.request.user, self.request.POST)
        #context['passwform'] = PasswordChangeForm(self.request.user, self.request.POST )
        return paginated_demands



class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'redico/profile4.html'
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
            demands = Demand.objectz.profile(self.request.user.pk, self.request.GET.o)
        except Exception as e:
            demands = Demand.objectz.profile(self.request.user.pk, '')
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
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Mot de passe changé avec succès!')
            return redirect('home:home')
        else:
            messages.error(request, 'Veuillez corriger!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,  'redico/profile4.html', {
        'passwform': form
    })