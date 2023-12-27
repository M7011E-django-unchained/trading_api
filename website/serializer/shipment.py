from rest_framework.serializers import (
    Serializer,
    HyperlinkedRelatedField

)
from website.models import Shipment
from django.contrib.auth.models import User


class ShipmentSerializer(Serializer):

    username = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Shipment
        fields = "__all__"
        read_only_fields = (
            "shipmentID",
            "timestamp",
        )
