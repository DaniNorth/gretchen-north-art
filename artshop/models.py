from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.apps import apps

class Artwork(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    medium = models.CharField(max_length=100, blank=True, null=True)
    collection = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)

    held_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="held_artworks")
    hold_expires_at = models.DateTimeField(null=True, blank=True)

    purchased_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="purchased_artworks")
    purchased_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_held(self):
        return self.held_by is not None and self.hold_expires_at and self.hold_expires_at > timezone.now()

    def hold(self, user):
        self.held_by = user
        self.hold_expires_at = timezone.now() + timedelta(minutes=15)
        self.save()

    def clear_hold_if_expired(self):
        if self.hold_expires_at and timezone.now() > self.hold_expires_at:
            self.held_by = None
            self.hold_expires_at = None
            self.save()
            CartItem = apps.get_model('artshop', 'CartItem')
            CartItem.objects.filter(artwork=self).delete()

    def mark_sold(self, user):
        self.is_active = False
        self.is_sold = True
        self.purchased_by = user
        self.purchased_at = timezone.now()
        self.held_by = None
        self.hold_expires_at = None
        self.save()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    artwork = models.OneToOneField(Artwork, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artwork.title} in {self.cart.user.username}'s cart"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artwork.title} in {self.wishlist.title}"