from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from authentication.models import CustomUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = data.get('email')
        user.google_id = sociallogin.account.uid
        user.profile_picture = data.get('picture')
        return user
