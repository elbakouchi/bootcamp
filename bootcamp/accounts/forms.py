from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import ReCaptchaField


class AllAuthSignInForm(LoginForm):

    captcha = ReCaptchaField()

    def save(self, request, user):
        user = super(AllAuthSignInForm, self).save(request)
        return user


class AllAuthSignUpForm(SignupForm):
    captcha = ReCaptchaField()

    def save(self, request, user):
        user = super(AllAuthSignUpForm, self).save(request)
        return user