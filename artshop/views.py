from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Artwork, Cart, CartItem

def home(request):
    artworks = Artwork.objects.all()
    # Clear expired holds for display
    for art in artworks:
        art.clear_hold_if_expired()
    return render(request, "artshop/home.html", {"artworks": artworks})

def artwork_detail(request, pk):
    art = get_object_or_404(Artwork, pk=pk)
    art.clear_hold_if_expired()
    return render(request, "artshop/artwork_detail.html", {"art": art})

@login_required
def add_to_cart(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    artwork.clear_hold_if_expired()

    if artwork.is_sold:
        messages.error(request, "This artwork has already been sold.")
        return redirect("home")

    if artwork.is_held and artwork.held_by != request.user:
        messages.warning(request, "This artwork is currently on hold for another customer.")
        return redirect("home")

    # Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Add artwork to cart or refresh the hold
    artwork.hold(request.user)
    CartItem.objects.get_or_create(cart=cart, artwork=artwork)

    messages.success(request, f"'{artwork.title}' has been added to your cart. You've got 15 minutes to check out.")
    return redirect("home")