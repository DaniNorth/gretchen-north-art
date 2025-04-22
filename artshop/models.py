from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Artwork(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title