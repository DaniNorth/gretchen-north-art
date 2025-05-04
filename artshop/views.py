from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomerProfile
from .forms import CustomerProfileForm

from .models import Artwork, Cart, CartItem

def home(request):
    artworks = Artwork.objects.all()
    for art in artworks:
        art.clear_hold_if_expired()
    return render(request, "artshop/home.html", {"artworks": artworks})

def artwork_detail(request, pk):
    art = get_object_or_404(Artwork, pk=pk)
    art.clear_hold_if_expired()

    remaining_hold = None
    if art.is_held and art.held_by == request.user:
        remaining_hold = art.hold_expires_at

    return render(request, "artshop/artwork_detail.html", {
        "art": art,
        "remaining_hold": remaining_hold,
    })

@login_required
def edit_profile(request):
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'artshop/edit_profile.html', {'form': form})

@login_required
def add_to_cart(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    artwork.clear_hold_if_expired()

    if artwork.is_sold:
        messages.error(request, "This artwork has already been sold.")
        return redirect("home")

    if artwork.is_held and artwork.held_by == request.user:
        remaining_hold = artwork.hold_expires_at.isoformat()
    else:
        remaining_hold = None

    cart, _ = Cart.objects.get_or_create(user=request.user)

    artwork.hold(request.user)

    CartItem.objects.get_or_create(cart=cart, artwork=artwork)

    messages.success(
        request,
        f"'{artwork.title}' has been added to your cart. You have 15 minutes to check out."
    )
    return redirect("artwork_detail", pk=artwork.pk)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('artwork')
    total = cart.total_price()

    return render(request, "artshop/cart.html", {
        "cart": cart,
        "items": items,
        "total": total
    })

@login_required
def checkout_view(request):
    return render(request, "artshop/checkout.html")