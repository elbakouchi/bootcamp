from django import forms

from ckeditor.widgets import CKEditorWidget

from bootcamp.demand.models import Demand


class DemandForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    verified = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    content = forms.Textarea()

    class Meta:
        model = Demand
        fields = ["title", "content", "category", "service", "status"]
