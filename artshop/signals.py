from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import CustomerProfile

@receiver(user_signed_up)
def create_profile_on_social_signup(request, user, **kwargs):
    CustomerProfile.objects.get_or_create(user=user)