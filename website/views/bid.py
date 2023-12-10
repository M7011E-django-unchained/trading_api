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
    # print('request.body=<{}>'.format(request.body[:10]))
    data = request.POST
    # print('first few characters=<{}>'.format(data[:10]))
    bid = {
        "auctionId": data.get('auctionId'),
        "bidder": data.get('bidder'),
        "bidderId": data.get('bidderId'),
        "bidAmount": data.get('bidAmount'),
    }

    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # bid = body['content']

    # bid = request.body

    # bid = json.loads(request.body)

    url = f'http://localhost:5000/api/v1/createBid'
    response = requests.post(url, json=bid)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids(request):
    url = f'http://localhost:5000/api/v1/getAllBids'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id(request, id):
    url = f'http://localhost:5000/api/v1/getAllBidsByAuctionId/{id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_bidder_id(request, id):
    url = f'http://localhost:5000/api/v1/getAllBidsByBidderId/{id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id_and_bidder_id(request, auctionId, bidderId):
    url = f'http://localhost:5000/api/v1/getAllbidsByAuctionIdAndBidderId/{auctionId}/{bidderId}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/getOneBid/{_id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def get_winnerby_auction_id(request, id):
    url = f'http://localhost:5000/api/v1/getWinnerbyAuctionId/{id}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def update_one_bid(request, _id):
    bid = {
        "auctionId": request.POST.get('auctionId'),
        "bidder": request.POST.get('bidder'),
        "bidderId": request.POST.get('bidderId'),
        "bidAmount": request.POST.get('bidAmount'),
        "bidTime": request.POST.get('bidTime'),
    }

    url = f'http://localhost:5000/api/v1/updateOneBid/{_id}'
    response = requests.patch(url, json=bid)
    data = response.json()
    return JsonResponse(data, safe=False)


def delete_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/deleteOneBid/{_id}'
    response = requests.delete(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def delete_all_bids_by_auction_id(request, id):
    url = f'http://localhost:5000/api/v1/deleteAllBidsByAuctionId/{id}'
    response = requests.delete(url)
    data = response.json()
    return JsonResponse(data, safe=False)
