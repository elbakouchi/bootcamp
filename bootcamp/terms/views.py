from django.forms import forms
from django.shortcuts import render, redirect

from bootcamp.terms.models import TermsOfService, Term


class TermsOfServiceForm(forms.ModelForm):
    class Meta:
        model = TermsOfService


def terms_of_service_view(request):
    if request.method == 'POST':
        form = TermsOfServiceForm(request.POST)
        if form.is_valid():
            user_membership = request.user.usermembership  # you don't need another view as User has OneToOne relation with UserMembership
            instance = form.save(commit=False)
            instance.user = request.user
            instance.term = Term.objects.last()
            instance.save()
            go_next = request.GET.get('next', None)  # handle redirection
            if go_next:
                return redirect(go_next)
            context = {
                'user_membership': user_membership,
                'form': form
            }
            return render(request, "index.html", context)
    else:
        form = TermsOfServiceForm()

    context = {
        'user_membership':  request.user.usermembership,
        'form': form,
    }
    return render(request, "index.html", context)
