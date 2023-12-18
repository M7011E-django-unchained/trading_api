from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import home, about_us, auctions, show_auction

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('auctions/', auctions, name='auctions'),
    path('auctions/<int:auction_id>', show_auction, name='show_auction'),
]
