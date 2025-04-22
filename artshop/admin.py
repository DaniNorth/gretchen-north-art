from django.contrib import admin
from .models import Artwork

# Register your models here.

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'description']