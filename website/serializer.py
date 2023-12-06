from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)
from django.contrib.auth.models import User
from .models import Member, Auction, Category, Subcategory

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

    def create(self, validated_data):
        subcategory = validated_data.get("subcategory")
        subcategory_object = Subcategory.objects.filter(
            subcategory_name=subcategory).values("category")
        category = Category.objects.filter(
            id=subcategory_object[0]["category"])

        return Auction.objects.create(**validated_data, category=category[0])

    class Meta:
        model = Auction
        fields = (
            "title",
            "auctionOwner",
            "description",
            "subcategory",
            "startingPrice",
            "buyOutPrice",
            "startTime",
            "endTime",
        )


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


# Subcategory serializers
class SubcategoryListSerializer(HyperlinkedModelSerializer):
    subcategory_name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="subcategory_name",
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Subcategory
        fields = ("id", "category", "subcategory_name")


class SubcategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("category", "subcategory_name")


class SubcategoryDetailSerializer(ModelSerializer):
    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    auctions = HyperlinkedIdentityField(
        view_name="subcategory-auction-list",
        lookup_field="subcategory_name",
    )

    class Meta:
        model = Subcategory
        fields = ("category", "subcategory_name", "auctions")


class SubcategoryFromCategory(HyperlinkedModelSerializer):
    subcategory_name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="subcategory_name",
    )

    class Meta:
        model = Subcategory
        fields = ("subcategory_name",)


# Category serializers
class CategorySerializer(HyperlinkedModelSerializer):
    name = HyperlinkedIdentityField(
        view_name="category-detail",
        lookup_field="name",
    )

    subcategories = SubcategoryFromCategory(
        source="parent_category", many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "subcategories")


class CategoryDetailSerializer(ModelSerializer):
    auctions = HyperlinkedIdentityField(
        view_name="category-auction-list",
        lookup_field="name",
    )

    class Meta:
        model = Category
        fields = ("id", "name", "auctions")


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


# Member/User serializers
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

    auctions = HyperlinkedIdentityField(
        view_name="member-auction-list",
        lookup_field="username",
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
            "auctions",
        )
