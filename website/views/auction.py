from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from website.serializer import (AuctionListSerializer,
                                AuctionDetailSerializer,
                                AuctionCreateSerializer, )

from website.models import Auction
from rest_framework.permissions import BasePermission


# Auction views


class AuctionPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return True
        elif view.action == "create":
            return request.user.is_authenticated


class AuctionEditPermission(BasePermission):
    def has_permission(self, request, view):
        # staff and superuser can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.method == "GET":
            return True
        return False  # you should not be able to edit any auctions

    def has_object_permission(self, request, view, obj):
        # staff and superuser can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.method == "GET":
            return True
        return False  # you should not be able to edit any auctions
        # if you want to be able to edit your auctions, use this:
        # return obj.auctionOwner == request.user


class AuctionList(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    permission_classes = (AuctionPermission,)

    def get_serializer_class(self):
        if self.action == "create":
            return AuctionCreateSerializer
        return self.serializer_class


class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AuctionEditPermission,)

    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    lookup_field = "auctionID"

    # add user to subscribed list of auction when auction is created
    def perform_create(self, serializer):
        serializer.save(subscribed=[self.request.user])


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


class MemberAuctionList(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    permission_classes = (AuctionEditPermission,)

    def get_queryset(self):
        username = self.kwargs["username"]
        return Auction.objects.filter(auctionOwner__username=username)

    def delete(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        resp_data = Auction.objects.filter(
            auctionOwner__username=username).delete()
        return Response(resp_data, status=status.HTTP_204_NO_CONTENT)
