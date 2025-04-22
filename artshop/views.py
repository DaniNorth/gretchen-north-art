from django.shortcuts import render
from .models import Artwork
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    artworks = Artwork.objects.all()
    return render(request, "artshop/home.html", {"artworks": artworks})

def artwork_detail(request, pk):
    art = get_object_or_404(Artwork, pk=pk)
    return render(request, "artshop/artwork_detail.html", {"art": art})