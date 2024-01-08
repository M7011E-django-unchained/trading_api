import datetime
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.utils import json
from website.models import Auction
from django.core.mail import send_mail

host = 'http://bidding_system:5000/api/v1/'


def bid_get_token_middleware(request):
    # THERE MUST BE A BETTER WAY TO DO THIS
    token = request.headers.get('authorization')
    return {"authorization": token}


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create_bid(request):
    data = json.loads(request.body)

    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    auction_id = data.get('auctionId')
    auction = Auction.objects.get(auctionID=auction_id)
    user = User.objects.get(id=data.get('bidderId'))
    bid_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if bid_time > auction.endTime.strftime("%Y-%m-%d %H:%M:%S"):
        return JsonResponse({"message": "Auction has ended"}, status=400)

    bid = {
        "auctionId": auction_id,
        "bidder": user.username,
        "bidderId": user.id,
        "bidAmount": data.get('bidAmount'),
        "bidTime": bid_time,
    }

    url = f'{host}createBid'
    response = requests.post(url, json=bid,
                             headers=bid_get_token_middleware(request))
    retrieved_data = response.json()

    if response.status_code == 201:
        # Email to bidder
        subject = f'You have placed a bid on {auction.title}'
        message = (
            f'You have placed a bid of ${bid.get("bidAmount")}'
            f' on {auction.title}'
        )
        from_email = 'django.unchained.project@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        # Email to subscribed users
        subject = f'A new bid has been placed on {auction.title}'
        message = (
            f'A new bid of ${bid.get("bidAmount")}'
            f' has been placed on {auction.title}'
        )
        from_email = 'django.unchained.project@gmail.com'
        recipient_list = [user.email for user in auction.subscribed.all()]
        send_mail(subject, message, from_email, recipient_list)

        auction.subscribed.add(user)
        auction.save()

    return JsonResponse(retrieved_data, safe=False)


@api_view(['GET'])
def get_all_bids(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getAllBids'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_one_bid(request, _id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getOneBid/{_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_all_bids_by_auction_id(request, auction_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getAllBidsByAuctionId/{auction_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_all_bids_by_bidder_id(request, bidder_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getAllBidsByBidderId/{bidder_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_all_bids_by_auction_id_and_bidder_id(request, auction_id, bidder_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getAllBids/'
    url += f'{auction_id}/{bidder_id}'
    response = requests.get(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_winner_by_auction_id(request, auction_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}getWinnerbyAuctionId/{auction_id}'
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
    if not request.user.is_staff or not request.user.is_superuser:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    data = json.loads(request.body)
    bid = {
        "auctionId": data.get('auctionId'),
        "bidder": data.get('bidder'),
        "bidderId": data.get('bidderId'),
        "bidAmount": data.get('bidAmount'),
        "bidTime": data.get('bidTime'),
    }

    url = f'{host}updateOneBid/{_id}'
    response = requests.patch(url, json=bid,
                              headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(['DELETE'])
def delete_one_bid(request, _id):
    if not request.user.is_staff or not request.user.is_superuser:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}deleteOneBid/{_id}'
    response = requests.delete(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(['DELETE'])
def delete_all_bids_by_auction_id(request, auction_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    url = f'{host}deleteAllBidsByAuctionId/{auction_id}'
    response = requests.delete(url, headers=bid_get_token_middleware(request))
    data = response.json()
    return JsonResponse(data, safe=False)
