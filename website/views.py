from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .serializer import (AuctionListSerializer,
                         AuctionDetailSerializer,
                         CategorySerializer,
                         CategoryCreateSerializer,
                         CategoryDetailSerializer,
                         SubcategoryListSerializer,
                         SubcategoryCreateSerializer,
                         SubcategoryDetailSerializer,
                         UserListSerializer,
                         UserDetailSerializer,
                         AuctionCreateSerializer,)

from .models import Auction, Category, Subcategory
from django.contrib.auth.models import User

# Create your views here.


# Auction views
class AuctionList(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return AuctionCreateSerializer
        return self.serializer_class


class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    lookup_field = "auctionID"


class CategoryAuctionList(generics.ListAPIView):
    serializer_class = AuctionListSerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Auction.objects.filter(category__name=name)


class SubcategoryAuctionList(generics.ListAPIView):
    serializer_class = AuctionListSerializer

    def get_queryset(self):
        subcat = self.kwargs["subcategory_name"]
        return Auction.objects.filter(subcategory__subcategory_name=subcat)


# Subcategory views
class SubcategoryList(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return SubcategoryCreateSerializer
        return self.serializer_class


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryDetailSerializer
    lookup_field = "subcategory_name"


# Category views
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


# Member views
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
