from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)

from .models import *


class AuctionListSerializer(HyperlinkedModelSerializer):
    auctionID = HyperlinkedIdentityField(
        view_name="auction_detail",
        lookup_field="auctionID",
    )

    category = HyperlinkedRelatedField(
        view_name="category_detail",
        many=True,
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Auction
        fields = (
            "auctionID",
            "title",
            "category",
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )


class AuctionDetailSerializer(ModelSerializer):
    category = HyperlinkedRelatedField(
        view_name="category_detail",
        many=True,
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Auction
        fields = "__all__"


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class MemberDetailSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ("profilePicPath",)


class UserListSerializer(HyperlinkedModelSerializer):
    username = HyperlinkedIdentityField(
        view_name="member_detail",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = ("username",)


class UserDetailSerializer(ModelSerializer):
    profilePicPath = MemberDetailSerializer(
        source="memeber",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "profilePicPath",
        )
