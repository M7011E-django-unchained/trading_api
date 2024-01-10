from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)
from django.contrib.auth.models import User
from website.models import Auction, Category, Subcategory


# Auction serializers


class AuctionListSerializer(HyperlinkedModelSerializer):
    auctionID = HyperlinkedIdentityField(
        view_name="auction-detail",
        lookup_field="auctionID",
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        many=False,
        queryset=Category.objects.filter(),
    )

    subcategory = HyperlinkedRelatedField(
        view_name="subcategory-detail",
        lookup_field="subcategory_name",
        queryset=Subcategory.objects.all(),
    )

    auctionOwner = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Auction
        fields = (
            "auctionID",
            "title",
            "auctionOwner",
            "description",
            "category",
            "subcategory",
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )


class AuctionCreateSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            "title",
            "auctionOwner",
            "description",
            "imagePath",
            "subcategory",
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )
        read_only_fields = ("auctionOwner",)

    def create(self, validated_data):
        subcategory = validated_data.get("subcategory")
        auction_owner = self.context["request"].user
        subcategory_object = Subcategory.objects.filter(
            subcategory_name=subcategory).values("category")
        category = Category.objects.filter(
            id=subcategory_object[0]["category"])

        auction = Auction.objects.create(**validated_data,
                                         category=category[0],
                                         auctionOwner=auction_owner)

        auction.subscribed.add(auction_owner)
        return auction


class AuctionDetailSerializer(ModelSerializer):
    subcategory = HyperlinkedRelatedField(
        view_name="subcategory-detail",
        many=False,
        lookup_field="subcategory_name",
        queryset=Subcategory.objects.all(),
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        many=False,
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    auctionOwner = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    subscribed = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        many=True,
        queryset=User.objects.all(),
    )

    class Meta:
        model = Auction
        fields = "__all__"
