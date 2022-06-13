from contact_form.forms import ContactForm, StringKeyedDict


class CustomContactForm(ContactForm):

    def get_message_dict(self) -> StringKeyedDict:
        message_dict = super(CustomContactForm, self).get_message_dict()
        message_dict.update('html_message', True)
        return message_dict
