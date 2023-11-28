from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
    SerializerMethodField,
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


## Subcategory serializers
class SubcategoryListByCategorySerializer(HyperlinkedModelSerializer):
    name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="name",
    )

    class Meta:
        model = SubCategory
        fields = "__all__"


class SubcategorySerializer(HyperlinkedModelSerializer):
    name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="name",
    )

    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = SubCategory
        fields = ("id", "name", "category")


class SubcategoryDetailSerializer(ModelSerializer):
    category = HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Category
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


class SubcategoryFromCategorySerializer(HyperlinkedModelSerializer):
    name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="name",
    )

    class Meta:
        model = SubCategory
        fields = ("name",)


class CategoryDetailSerializer(ModelSerializer):
    # TODO add subcategory list
    subcategories = SubcategoryFromCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "subcategories")


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


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
