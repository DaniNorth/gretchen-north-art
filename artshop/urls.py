from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("artwork/<int:pk>/", views.artwork_detail, name="artwork_detail"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
]