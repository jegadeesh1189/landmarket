from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .models import LandListing, LandPhoto, Profile, Wishlist
from .emails import send_welcome_email,send_wishlist_notification
from .forms import (VendorRegisterForm, BuyerRegisterForm,
                   LandListingForm, LandPhotoForm)


def home(request):
    listings = LandListing.objects.filter(status='available').prefetch_related('photos')[:6]
    return render(request, 'home.html', {'listings': listings})


def vendor_register(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email(user,'vendor')
            messages.success(request, 'Vendor account created! Welcome.')
            return redirect('vendor_dashboard')
    else:
        form = VendorRegisterForm()
    return render(request, 'vendor_register.html', {'form': form})


def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email(user,'buyer')
            messages.success(request, 'Buyer account created! Browse listings now.')
            return redirect('land_list')
    else:
        form = BuyerRegisterForm()
    return render(request, 'buyer_register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                profile = user.profile
                if profile.user_type == 'vendor':
                    return redirect('vendor_dashboard')
            except:
                pass
            return redirect('land_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def vendor_dashboard(request):
    try:
        if request.user.profile.user_type != 'vendor':
            messages.error(request, 'Access denied. Vendors only.')
            return redirect('home')
    except:
        return redirect('home')

    listings = LandListing.objects.filter(vendor=request.user).prefetch_related('photos')
    return render(request, 'vendor_dashboard.html', {'listings': listings})


@login_required
def add_listing(request):
    try:
        if request.user.profile.user_type != 'vendor':
            return redirect('home')
    except:
        return redirect('home')

    if request.method == 'POST':
        land_form = LandListingForm(request.POST)
        if land_form.is_valid():
            land = land_form.save(commit=False)
            land.vendor = request.user
            land.save()
            # Save multiple photos
            for img in request.FILES.getlist('images'):
                LandPhoto.objects.create(land=land, image=img)
            messages.success(request, 'Land listing posted successfully!')
            return redirect('vendor_dashboard')
    else:
        land_form = LandListingForm()

    gmaps_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'add_listing.html', {
        'land_form': land_form,
        'gmaps_key': gmaps_key,
    })


@login_required
def edit_listing(request, pk):
    land = get_object_or_404(LandListing, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = LandListingForm(request.POST, instance=land)
        if form.is_valid():
            form.save()
            for img in request.FILES.getlist('images'):
                LandPhoto.objects.create(land=land, image=img)
            messages.success(request, 'Listing updated!')
            return redirect('vendor_dashboard')
    else:
        form = LandListingForm(instance=land)
    return render(request, 'add_listing.html', {
        'land_form': form,
        'land': land,
        'gmaps_key': settings.GOOGLE_MAPS_API_KEY,
    })


@login_required
def delete_listing(request, pk):
    land = get_object_or_404(LandListing, pk=pk, vendor=request.user)
    if request.method == 'POST':
        land.delete()
        messages.success(request, 'Listing deleted.')
    return redirect('vendor_dashboard')

def land_list(request):
    query = request.GET.get('q', '')
    land_type = request.GET.get('type', '')
    min_price = request.GET.get('min_price', '')  # NEW
    max_price = request.GET.get('max_price', '')  # NEW

    listings = LandListing.objects.filter(status='available').prefetch_related('photos')

    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(city__icontains=query) | Q(state__icontains=query)
        )
    if land_type:
        listings = listings.filter(land_type=land_type)
    if min_price:  # NEW
        listings = listings.filter(price__gte=min_price)
    if max_price:  # NEW
        listings = listings.filter(price__lte=max_price)

    return render(request, 'land_list.html', {
        'listings': listings,
        'query': query,
        'land_type': land_type,
        'min_price': min_price,  # NEW
        'max_price': max_price,  # NEW
        'type_choices': LandListing.LAND_TYPE_CHOICES,
    })

def land_detail(request, pk):
    land = get_object_or_404(LandListing, pk=pk)
    photos = land.photos.all()
    try:
        vendor_profile = land.vendor.profile
    except:
        vendor_profile = None
    return render(request, 'land_detail.html', {
        'land': land,
        'photos': photos,
        'vendor_profile': vendor_profile,
        'gmaps_key': settings.GOOGLE_MAPS_API_KEY,
    })

@login_required
def toggle_wishlist(request, pk):
    land = get_object_or_404(LandListing, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, land=land)
    if not created:
        obj.delete()
        messages.info(request, 'Removed from wishlist.')
    else:
        messages.success(request, 'Added to wishlist! ❤️')
        send_wishlist_notification(land.vendor,request.user,land)
    return redirect('land_detail', pk=pk)


@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user).select_related('land').prefetch_related('land__photos')
    return render(request, 'wishlist.html', {'items': items})