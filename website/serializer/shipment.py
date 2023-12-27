from rest_framework.serializers import (
    ModelSerializer

)
from website.models import Shipment


class ShipmentSerializer(ModelSerializer):

    class Meta:
        model = Shipment
        fields = "__all__"
        extra_kwargs = {'auctionID': {'required': True}}
