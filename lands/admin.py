from django.contrib import admin
from .models import Profile, LandListing, LandPhoto


class LandPhotoInline(admin.TabularInline):
    model = LandPhoto
    extra = 1


@admin.register(LandListing)
class LandListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor', 'city', 'price', 'status', 'created_at']
    list_filter = ['status', 'land_type', 'city']
    search_fields = ['title', 'vendor__username', 'city']
    inlines = [LandPhotoInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone_number']
    list_filter = ['user_type']


admin.site.register(LandPhoto)
