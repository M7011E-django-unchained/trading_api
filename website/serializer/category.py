from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
)

from website.models import Category
from .subcategory import SubcategoryFromCategory

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
