from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from website.serializer import (AuctionListSerializer,
                                AuctionDetailSerializer,
                                AuctionCreateSerializer, )

from website.models import Auction
from rest_framework.permissions import BasePermission, IsAuthenticated
from .helpers import idempotent_check, IdempotencyException


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
            if idempotent_check(self.request):
                return AuctionCreateSerializer
            raise IdempotencyException
        return self.serializer_class


class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AuctionEditPermission,)

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


class AuctionSubscribe(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    lookup_field = "auctionID"

    def put(self, request, *args, **kwargs):
        auction = self.get_object()
        user = request.user
        if user in auction.subscribed.all() and auction.auctionOwner != user:
            auction.subscribed.remove(user)
            msg = f'You are no longer subscribed to "{auction.title}"'
            return Response(
                {
                    "message": msg},
                status=status.HTTP_200_OK)
        elif auction.auctionOwner == user:
            msg = 'You are always subscribed to your own auctions'
            return Response(
                {
                    "message": msg},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            auction.subscribed.add(user)
            msg = f'You are now subscribed to "{auction.title}"'
            return Response(
                {
                    "message": msg},
                status=status.HTTP_200_OK)
