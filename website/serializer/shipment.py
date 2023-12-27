from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
    ModelSerializer

)
from website.models import Shipment, Auction
from django.contrib.auth.models import User


class ShipmentListSerializer(ModelSerializer):
    shipmentID = HyperlinkedIdentityField(
        view_name="shipment-detail",
        lookup_field="pk",
    )

    class Meta:
        model = Shipment
        fields = ("shipmentID",)


class ShipmentCreateSerializer(HyperlinkedModelSerializer):

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
