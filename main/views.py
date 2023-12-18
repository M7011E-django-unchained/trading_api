from django.db.models import Count
from django.shortcuts import render

from website.models import Auction
from website.views import bid


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
    context = {
        'auctions': Auction.objects.all()
    }

    return render(request, 'pages/auctions.html', context)


def show_auction(request, auction_id):
    """Display individual auction
    :param request:
    :param auction_id:
    :return:
    """
    auction = Auction.objects.get(auctionID=auction_id)
    context = {
        'auction': auction,
    }

    return render(request, 'pages/show_auction.html', context)
