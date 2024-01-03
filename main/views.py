from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from website.models import Auction


# Create your views here.
def home(request):
    context = {
        'title': 'Welcome to Django Unchained, a trading API',
    }
    return render(request, 'pages/home.html', context)


# Create your views here.
def about_us(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'pages/about_us.html', context)


def auctions(request):
    """Display a list of auctions
    :param request:
    :return:
    """
    auction_list = Auction.objects.select_related('auctionOwner', 'category',
                                                  'subcategory',
                                                  'winnerID').prefetch_related(
        'subscribed').all()
    context = {
        'auctions': auction_list,
    }

    return render(request, 'pages/auctions.html', context)


def show_auction(request, auction_id):
    """Display individual auction
    :param request:
    :param auction_id:
    :return:
    """
    auction = Auction.objects.select_related('auctionOwner', 'category',
                                             'subcategory',
                                             'winnerID').prefetch_related(
        'subscribed').get(auctionID=auction_id)

    context = {
        'auction': auction,
    }

    return render(request, 'pages/show_auction.html', context)


def all_users(request):
    """Display all users
    :param request:
    :return:
    """
    users = User.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'pages/all_users.html', context)


def show_user(request, user_id):
    """Display individual user
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
    }

    return render(request, 'pages/show_user.html', context)
