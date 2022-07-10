from django.contrib.auth.models import User
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount



class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        # email_domain = sociallogin.user.email
        # print(email_domain)
        # value = request.COOKIES.get('store_name')
        # print('store', value)
        # print(SocialAccount.objects.filter(user=sociallogin.user))
        pass