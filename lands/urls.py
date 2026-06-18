from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/vendor/', views.vendor_register, name='vendor_register'),
    path('register/buyer/', views.buyer_register, name='buyer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/add/', views.add_listing, name='add_listing'),
    path('vendor/edit/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('vendor/delete/<int:pk>/', views.delete_listing, name='delete_listing'),
    path('lands/', views.land_list, name='land_list'),
    path('lands/<int:pk>/', views.land_detail, name='land_detail'),
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('wishlist/toggle/<int:pk>/',views.toggle_wishlist, name='toggle_wishlist'),
]