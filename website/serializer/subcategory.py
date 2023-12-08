from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)
from website.models import Category, Subcategory

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
