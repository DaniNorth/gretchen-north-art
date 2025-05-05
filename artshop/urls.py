from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("artwork/<int:pk>/", views.artwork_detail, name="artwork_detail"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("checkout/complete/", views.checkout_complete_view, name="checkout_complete")
]