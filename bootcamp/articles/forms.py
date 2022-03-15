from django import forms

from markdownx.fields import MarkdownxFormField

from bootcamp.articles.models import Article
from bootcamp.demand.models import Demand


class SuggestedRevisionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.HiddenInput())
    status = forms.CharField(widget=forms.HiddenInput(), required=False, initial="P")
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    content = forms.CharField(widget=forms.HiddenInput())
    demand = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Demand.objects.get_published())

    class Meta:
        model = Article
        fields = ["title", "content", "demand", "status", "edited"]


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    content = MarkdownxFormField()

    class Meta:
        model = Article
        fields = ["title", "content", "status", "edited"]
