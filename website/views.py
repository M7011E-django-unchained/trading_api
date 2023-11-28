from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from .models import *

# Create your views here.


## Auction views
class AuctionList(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer


class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    lookup_field = "auctionID"


## Category views
class CategoryList(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        return self.serializer_class


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "name"


## Subcategory views
class SubcategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategoryDetailSerializer
    lookup_field = "name"


## Member views
class MemberList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class MemberDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "username"


class MemberAuctionList(generics.ListAPIView):
    serializer_class = AuctionListSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        return Auction.objects.filter(auctionOwner__username=username)
