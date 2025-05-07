import os
import uuid
import logging
from dotenv import load_dotenv
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import CustomerProfile, Artwork, Cart, CartItem, Wishlist, WishlistItem
from .forms import CustomerProfileForm, WishlistForm
from artshop.square_client import client
from square.core.api_error import ApiError

load_dotenv()
logger = logging.getLogger(__name__)

def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'newest')

    artworks = Artwork.objects.filter(is_sold=False)
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        artworks = artworks.filter(category__iexact=category)
    if sort == 'price_low':
        artworks = artworks.order_by('price')
    elif sort == 'price_high':
        artworks = artworks.order_by('-price')
    elif sort == 'oldest':
        artworks = artworks.order_by('created_at')
    else:  # Default to newest
        artworks = artworks.order_by('-created_at')

    for art in artworks:
        art.clear_hold_if_expired()
    categories = Artwork.objects.values_list('category', flat=True).distinct()

    return render(request, "artshop/home.html", {
        "artworks": artworks,
        "query": query,
        "category": category,
        "sort": sort,
        "categories": categories,
    })

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
        messages.success(request, "Your profile was updated successfully.")
        return redirect('profile')
    return render(request, 'artshop/edit_profile.html', {'form': form})

@login_required
def add_to_cart(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    artwork.clear_hold_if_expired()

    if artwork.is_sold:
        messages.error(request, "This artwork has already been sold.")
        return redirect("home")
    if artwork.is_held and artwork.held_by != request.user:
        messages.error(request, "This artwork is currently on hold by another customer.")
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

        for item in items:
            item.artwork.hold(request.user)

        if not items.exists():
            return render(request, "artshop/checkout_error.html", {
                "errors": [{"detail": "Your cart is empty."}]
            })
        total_amount_cents = int(sum(item.artwork.price for item in items) * 100)
        response = client.payments.create(
            idempotency_key=str(uuid.uuid4()),
            source_id="cnon:card-nonce-ok",  # remember to update with Gretchen's real api once live
            amount_money={
                "amount": total_amount_cents,
                "currency": "USD"
            },
            location_id=os.environ.get("SQUARE_LOCATION_ID"),
            note=f"Purchase by {request.user.username}",
            autocomplete=True
        )

        for item in items:
            item.artwork.mark_sold(request.user)
            item.delete()

        return render(request, "artshop/checkout_complete.html", {
            "confirmation": response.payment.id,
        })

    except ApiError as e:
        logger.error("Square API Error:")
        for error in e.errors:
            logger.error(f"{error.category} - {error.code}: {error.detail}")
        return render(request, "artshop/checkout_error.html", {
            "errors": [{"detail": error.detail, "code": error.code} for error in e.errors]
        })
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

@login_required
def profile_view(request):
    profile = request.user.profile
    wishlists = request.user.wishlists.all()
    purchases = Artwork.objects.filter(purchased_by=request.user).order_by('-purchased_at')
    cart = Cart.objects.get(user=request.user)

    return render(request, 'artshop/profile.html', {
        'profile': profile,
        'wishlists': wishlists,
        'purchases': purchases,
        'cart': cart,
    })

#still having issues with turing my single page into a modal, come back to this
@login_required
def create_wishlist(request):
    form = WishlistForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        wishlist = form.save(commit=False)
        wishlist.user = request.user
        wishlist.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "toast": "Wishlist created!"})
        return redirect("profile")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("artshop/partials/modal_form.html", {
            "form": form,
            "title": "Create Wishlist",
            "submit_label": "Save Wishlist",
        }, request=request)
        return JsonResponse({"success": False, "html": html})
    if not request.headers.get("x-requested-with") == "XMLHttpRequest":
        return redirect("profile")

    return render(request, "artshop/wishlist_form.html", {"form": form})

@login_required
def wishlist_detail(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    items = wishlist.items.select_related('artwork')
    return render(request, 'artshop/wishlist_detail.html', {
        'wishlist': wishlist,
        'items': items
    })

@login_required
def edit_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    form = WishlistForm(request.POST or None, instance=wishlist)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('wishlist_detail', pk=wishlist.pk)
    return render(request, 'artshop/wishlist_form.html', {
        'form': form,
        'wishlist': wishlist
    })

@login_required
@require_POST
def delete_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    wishlist.delete()
    return redirect('profile')

@login_required
def add_to_wishlist(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if request.method == "POST":
        wishlist_id = request.POST.get("wishlist_id")
        wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
        WishlistItem.objects.get_or_create(wishlist=wishlist, artwork=artwork)
        messages.success(request, f"Added to wishlist: {wishlist.title}")
        return redirect("home")
    
    messages.warning(request, "Invalid request method.")
    return redirect("home")

@login_required
@require_POST
def remove_from_wishlist(request, wishlist_id, artwork_id):
    wishlist = get_object_or_404(Wishlist, pk=wishlist_id, user=request.user)
    wishlist.items.filter(artwork__id=artwork_id).delete()
    messages.success(request, "Artwork removed from wishlist.")
    return redirect("profile")

def about(request):
    return render(request, "artshop/about.html")