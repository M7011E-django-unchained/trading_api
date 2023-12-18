import datetime
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.utils import json
from website.models import Auction


def bid_get_token_middleware(request):
    # THERE MUST BE A BETTER WAY TO DO THIS
    token = request.headers.get('authorization')
    return {"authorization": token}


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create_bid(request):
    data = json.loads(request.body)

    auction_id = data.get('auctionId')
    auction = Auction.objects.get(auctionID=auction_id)
    user = User.objects.get(id=data.get('bidderId'))

    bid = {
        "auctionId": auction_id,
        "bidder": user.username,
        "bidderId": user.id,
        "bidAmount": data.get('bidAmount'),
        "bidTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    url = 'http://localhost:5000/api/v1/createBid'
    response = requests.post(url, json=bid,
                             headers=bid_get_token_middleware(request))
    retrieved_data = response.json()

    if response.status_code == 201:
        auction.subscribed.add(user)
        auction.save()

    return JsonResponse(retrieved_data, safe=False)


def get_all_bids(request):
    url = 'http://localhost:5000/api/v1/getAllBids'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


def get_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/getOneBid/{_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/getAllBidsByAuctionId/{auction_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_bidder_id(request, bidder_id):
    url = f'http://localhost:5000/api/v1/getAllBidsByBidderId/{bidder_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


def get_all_bids_by_auction_id_and_bidder_id(request, auction_id, bidder_id):
    url = 'http://localhost:5000/api/v1/getAllBids/'
    url += f'{auction_id}/{bidder_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


def get_winner_by_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/getWinnerbyAuctionId/{auction_id}'
    auction = Auction.objects.get(auctionID=auction_id)
    end_time = auction.endTime.strftime("%Y-%m-%d %H:%M:%S")
    print(end_time)
    body = {
        "endTime": end_time
    }

    response = requests.get(url, json=body,
                            headers=bid_get_token_middleware(request))

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
    response = requests.patch(url, json=bid,
                              headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_one_bid(request, _id):
    url = f'http://localhost:5000/api/v1/deleteOneBid/{_id}'
    response = requests.delete(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_all_bids_by_auction_id(request, auction_id):
    url = f'http://localhost:5000/api/v1/deleteAllBidsByAuctionId/{auction_id}'
    response = requests.delete(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)
