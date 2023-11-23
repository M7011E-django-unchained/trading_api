from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
)

from .models import *


class AuctionSerializer(HyperlinkedModelSerializer):
    category = HyperlinkedRelatedField(
        view_name="category_detail", read_only=True, lookup_field="name"
    )

    class Meta:
        model = Auction
        fields = (
            "auctionID",
            "title",
            "description",
            "imagePath",
            "category",
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
