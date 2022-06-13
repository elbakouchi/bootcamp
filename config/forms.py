from contact_form.forms import ContactForm, StringKeyedDict
from django.template import loader


class CustomContactForm(ContactForm):
    def message_html(self) -> str:
        """
        Render the body of the message to a string.

        """
        template_name = 'contact_form/contact_form.html'
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def get_message_dict(self) -> StringKeyedDict:
        message_dict = super(CustomContactForm, self).get_message_dict()
        html_message = self.message_html()
        message_dict.update({'html_message': html_message})
        return message_dict
