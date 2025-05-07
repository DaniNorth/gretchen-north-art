from django.utils import timezone
from .models import Artwork

def hold_timer(request):
    if request.user.is_authenticated:
        held_artworks = Artwork.objects.filter(
            held_by=request.user,
            hold_expires_at__gt=timezone.now()
        ).order_by('-hold_expires_at')
        
        if held_artworks.exists():
            return {
                "cart_hold_expires_at": held_artworks.first().hold_expires_at
            }

    return {}

# produced by ChatGPT to accomany my issues with getting the countdown time to work properly