from django.urls import path

from .views import home, about_us, auctions, show_auction, all_users, show_user

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('auctions/', auctions, name='auctions'),
    path('auctions/<int:auction_id>', show_auction, name='show_auction'),
    path('all_users/', all_users, name='all_users'),
    path('user/<int:user_id>/', show_user, name='show_user'),
]
