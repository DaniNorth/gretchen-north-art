import os
import uuid
import logging
from dotenv import load_dotenv
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomerProfile, Artwork, Cart, CartItem
from .forms import CustomerProfileForm
from artshop.square_client import client
from square.core.api_error import ApiError

load_dotenv()
logger = logging.getLogger(__name__)

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
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    form = CustomerProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'artshop/edit_profile.html', {'form': form})

@login_required
def add_to_cart(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    artwork.clear_hold_if_expired()

    if artwork.is_sold:
        messages.error(request, "This artwork has already been sold.")
        return redirect("home")

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

#Sqaure checkout logic, remember to update the .env sqaure access token to Gretchens once in production

@login_required
def checkout_view(request):
    try:
        cart = request.user.cart
        items = cart.items.select_related('artwork')

        if not items.exists():
            return render(request, "artshop/checkout_error.html", {
                "errors": [{"detail": "Your cart is empty."}]
            })

        total_amount_cents = int(sum(item.artwork.price for item in items) * 100)

        response = client.payments.create(
            idempotency_key=str(uuid.uuid4()),
            source_id="cnon:card-nonce-ok",  # 🔁 Replace this with a real token in production
            amount_money={
                "amount": total_amount_cents,
                "currency": "USD"
            },
            location_id=os.environ.get("SQUARE_LOCATION_ID"),
            note=f"Purchase by {request.user.username}",
            autocomplete=True  # Set to False if you want to delay capture
        )

        # Mark artworks as sold
        for item in items:
            item.artwork.mark_sold(request.user)
            item.delete()

        return render(request, "artshop/checkout_complete.html", {
            "confirmation": response.payment.id,
        })

    except ApiError as e:
        logger.error("Square API Error:")
        for error in e.errors:
            logger.error(f"{error['category']} - {error['code']}: {error['detail']}")
        return render(request, "artshop/checkout_error.html", {"errors": e.errors})

    except Exception as e:
        logger.exception("Unexpected checkout exception")
        return render(request, "artshop/checkout_error.html", {
            "errors": [{"detail": str(e)}]
        })
    
@login_required
def checkout_complete_view(request):
    cart = request.user.cart
    for item in cart.items.select_related("artwork"):
        item.artwork.mark_sold(request.user)
        item.delete()
    return render(request, "artshop/checkout_complete.html")