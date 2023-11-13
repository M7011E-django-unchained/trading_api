from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import *


class MemberSerializer(ModelSerializer):
    Username = StringRelatedField(many=False)

    class Meta:
        model = Member
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AuctionDetailSerializer(ModelSerializer):
    Category = StringRelatedField(many=True)

    class Meta:
        model = Auction
        fields = "__all__"


class AuctionWriteSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            "Title",
            "AuctionOwner",
            "Description",
            "ImagePath",
            "Category",
            "StartingPrice",
            "BuyOutPrice",
            "EndTime",
        )


class ShipmentSerializer(ModelSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"
