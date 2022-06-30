from allauth.account.forms import LoginForm
from captcha.fields import ReCaptchaField


class AllAuthSignInForm(LoginForm):

    captcha = ReCaptchaField()

    def save(self, request, user):
        user = super(AllAuthSignInForm, self).save(request)
        return user