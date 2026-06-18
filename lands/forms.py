from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, LandListing, LandPhoto


class VendorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type='vendor',
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
            )
        return user


class BuyerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type='buyer',
                phone_number=self.cleaned_data['phone_number'],
            )
        return user


class LandListingForm(forms.ModelForm):
    class Meta:
        model = LandListing
        fields = ['title', 'description', 'price', 'area_sqft',
                  'land_type', 'status', 'latitude', 'longitude',
                  'address_text', 'city', 'state', 'country']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': 'e.g. 13.082680'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': 'e.g. 80.270718'}),
        }


class LandPhotoForm(forms.ModelForm):
    class Meta:
        model = LandPhoto
        fields = ['image', 'caption']