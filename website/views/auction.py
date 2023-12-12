from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from website.serializer import (AuctionListSerializer,
                                AuctionDetailSerializer,
                                AuctionCreateSerializer, )

from website.models import Auction


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


class AuctionDeleteByUser(generics.DestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        return Auction.objects.filter(auctionOwner__username=username)
