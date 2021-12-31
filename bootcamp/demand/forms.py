from django import forms

from markdownx.fields import MarkdownxFormField

from bootcamp.demand.models import Demand


class DemandForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    content = MarkdownxFormField()

    class Meta:
        model = Demand
        fields = ["title", "content", "category", "service", "status", "edited"]
