from allauth.account.utils import perform_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

from bootcamp.users.models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        super(SocialAccountAdapter, self).get_connect_redirect_url(request, socialaccount)
        print(socialaccount)
        assert request.user.is_authenticated
        url = reverse("home:home")
        return url

    def populate_user(self, request, sociallogin, data):
        print(data)
        return super(SocialAccountAdapter, self).populate_user(request, sociallogin, data)

    def pre_social_login(self, request, sociallogin):
        super(SocialAccountAdapter, self).pre_social_login(request, sociallogin)
        print(sociallogin)
        user = sociallogin.user
        #if user.id:
        #    return
        try:
            user = User.objects.get(
                email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            pass
