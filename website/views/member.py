from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from website.serializer import (AuctionListSerializer,
                                UserListSerializer,
                                UserDetailSerializer,
                                )
from website.models import Auction
from django.contrib.auth.models import User


class MemberList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class MemberDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "username"


class MemberAuctionList(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        return Auction.objects.filter(auctionOwner__username=username)

    def delete(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        resp_data = Auction.objects.filter(
            auctionOwner__username=username).delete()
        print(resp_data)
        return Response(resp_data, status=status.HTTP_204_NO_CONTENT)
