from contact_form.forms import ContactForm, StringKeyedDict
from django.template import loader
from django.core.mail import send_mail
from captcha.fields import ReCaptchaField
from django import forms, http
from phonenumber_field.formfields import PhoneNumberField


class CustomContactForm(ContactForm):
    captcha = ReCaptchaField()

    def save(self, fail_silently: bool = False) -> None:
        try:
            kwargs = self.get_message_dict()
            if not 'CrytoKagKag' in kwargs.get('subject'):
                send_mail(fail_silently=fail_silently, **kwargs)
        except: pass        

    def message_html(self) -> str:
        """
        Render the body of the message to a string.

        """
        template_name = 'contact_form/contact_form.html'
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def get_message_dict(self) -> StringKeyedDict:
        try:
            message_dict = super(CustomContactForm, self).get_message_dict()
            html_message = self.message_html()
            message_dict.update({'html_message': html_message})
            return message_dict
        except: pass    

class CustomServicesForm(CustomContactForm):
    #captcha = ReCaptchaField()
    phone = PhoneNumberField()

    subject_template_name = "services/services_form_subject.txt"

    template_name = "services/services_form.txt"

    def message_html(self) -> str:
        """
        Render the body of the message to a string.
        """
        template_name = 'services/services_form.html'
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )



from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from typing import Any, Dict, List, Optional

class CustomServicesForm2(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), max_length=150)
    email = forms.EmailField(max_length=150)
    phone = PhoneNumberField()
    message = forms.Textarea()
    # captcha = ReCaptchaField()
    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "services/services_form_subject.txt"

    def __init__(
        self,
        data: Optional[StringKeyedDict] = None,
        files: Optional[StringKeyedDict] = None,
        request: Optional[http.HttpRequest] = None,
        recipient_list: Optional[List[str]] = None,
        *args,
        **kwargs
    ):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        self.request = request
        if recipient_list is not None:
            self.recipient_list = recipient_list
        super().__init__(data=data, files=files, *args, **kwargs)

    def get_context(self) -> StringKeyedDict:
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        return dict(self.cleaned_data, site=get_current_site(self.request))

    def save(self, fail_silently: bool = False) -> None:
        kwargs = self.get_message_dict()
        if not 'CrytoKagKag' in kwargs.get('subject'):
         send_mail(fail_silently=fail_silently, **kwargs)

    def message_html(self) -> str:
        """
        Render the body of the message to a string.
        """
        template_name = 'redico/services/services_form.html'
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def get_message_dict(self) -> StringKeyedDict:
        message_dict = dict()
        html_message = self.message_html()
        message_dict.update({'html_message': html_message})
        return message_dict