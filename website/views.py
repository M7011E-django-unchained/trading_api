from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import *
from .models import *

# Create your views here.


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "Auction-List": "/auction-list/",
        "Auction-Detail": "/auction-detail/<str:auctionID>",
        "Auction-Create": "/auction-create/",
        "Auction-Update": "/auction-update/<str:auctionID>",
        "Auction-Delete": "/auction-delete/<str:auctionID>",
        "User-List": "/user-list/",
        "User-Create": "/user-create/",
    }
    return Response(api_urls)


@api_view(["GET"])
def auctionList(request):
    auctions = Auction.objects.all()
    serializer = AuctionDetailSerializer(auctions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def auctionDetail(request, id):
    auctions = Auction.objects.get(AuctionID=id)
    serializer = AuctionDetailSerializer(auctions, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def auctionCreate(request):
    serializer = AuctionWriteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def auctionUpdate(request, id):
    auction = Auction.objects.get(AuctionID=id)
    serializer = AuctionWriteSerializer(instance=auction, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def auctionDelete(request, id):
    auction = Auction.objects.get(AuctionID=id)
    auction.delete()

    return Response("Auction with id:" + id + " deleted")


@api_view(["GET"])
def userList(request):
    users = Member.objects.all()
    serializer = MemberSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def userDetail(request, id):
    user = Member.objects.get(UserID=id)
    serializer = MemberSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def userCreate(request):
    serializer = MemberSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
