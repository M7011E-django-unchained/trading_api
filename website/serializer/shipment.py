from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer

)
from website.models import Shipment, Auction
from django.contrib.auth.models import User


class ShipmentSerializer(HyperlinkedModelSerializer):

    username = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    auctionID = HyperlinkedRelatedField(
        view_name="auction-detail",
        lookup_field="auctionID",
        queryset=Auction.objects.all(),
    )

    class Meta:
        model = Shipment
        fields = "__all__"
        extra_kwargs = {'auctionID': {'required': True}}


class ShipmentDetailSerializer(ModelSerializer):

    username = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    auctionID = HyperlinkedRelatedField(
        view_name="auction-detail",
        lookup_field="auctionID",
        queryset=Auction.objects.all(),
    )

    class Meta:
        model = Shipment
        fields = "__all__"
