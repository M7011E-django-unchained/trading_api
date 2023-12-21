from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField
)
from django.contrib.auth.models import User
from website.models import Shipment, Auction


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
        read_only_fields = (
            "shipmentID",
            "timestamp",
        )
