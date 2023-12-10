import datetime

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create_bid(request):
    data = json.loads(request.body)
    bid = {
        "auctionId": data.get('auctionId'),
        "bidder": data.get('bidder'),
        "bidderId": data.get('bidderId'),
        "bidAmount": data.get('bidAmount'),
        "bidTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    url = 'http://localhost:5000/api/v1/createBid'
    response = requests.post(url, json=bid)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids(request):
    url = 'http://localhost:5000/api/v1/getAllBids'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/getOneBid/{_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/getAllBidsByAuctionId/{auction_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_bidder_id(request, bidder_id):
    url = f'http://localhost:5000/api/v1/getAllBidsByBidderId/{bidder_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id_and_bidder_id(request, auction_id, bidder_id):
    url = 'http://localhost:5000/api/v1/getAllBids/'
    url += f'{auction_id}/{bidder_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_winnerby_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/getWinnerbyAuctionId/{auction_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(['POST'])
def update_one_bid(request, _id):
    data = json.loads(request.body)
    bid = {
        "auctionId": data.get('auctionId'),
        "bidder": data.get('bidder'),
        "bidderId": data.get('bidderId'),
        "bidAmount": data.get('bidAmount'),
        "bidTime": data.get('bidTime'),
    }

    url = f'http://localhost:5000/api/v1/updateOneBid/{_id}'
    response = requests.patch(url, json=bid)
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/deleteOneBid/{_id}'
    response = requests.delete(url)
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_all_bids_by_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/deleteAllBidsByAuctionId/{auction_id}'
    response = requests.delete(url)
    data = response.json()
    return JsonResponse(data, safe=False)
