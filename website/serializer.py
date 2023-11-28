from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)

from .models import *

## Auction serializers


class AuctionListSerializer(HyperlinkedModelSerializer):
    auctionID = HyperlinkedIdentityField(
        view_name="auction-detail",
        lookup_field="auctionID",
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        many=True,
        lookup_field="name",
        queryset=Category.objects.all(),
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
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )


class AuctionDetailSerializer(ModelSerializer):
    category = HyperlinkedRelatedField(
        view_name="category-detail",
        many=True,
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


## Category serializers
class CategorySerializer(HyperlinkedModelSerializer):
    name = HyperlinkedIdentityField(
        view_name="category-detail",
        lookup_field="name",
    )

    class Meta:
        model = Category
        fields = ("id", "name")


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


## Subcategory serializers


class SubcategorySerializer(HyperlinkedModelSerializer):
    id = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="id",
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = SubCategory
        fields = ("id", "name", "category")


## Member/User serializers


class MemberDetailSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ("profilePicPath",)


class UserListSerializer(HyperlinkedModelSerializer):
    username = HyperlinkedIdentityField(
        view_name="member-detail",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = ("username",)


class UserDetailSerializer(ModelSerializer):
    profilePicPath = MemberDetailSerializer(
        source="member",
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
