from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    SlugRelatedField,
)
from django.urls import reverse
from website.models import Category, Subcategory

# Subcategory serializers


class categoryTranslator(SlugRelatedField):
    def to_representation(self, value):
        return self.context['request'].build_absolute_uri(
            reverse('category-detail', kwargs={'name': value.name}))


class SubcategoryListSerializer(HyperlinkedModelSerializer):
    subcategory_name = HyperlinkedIdentityField(
        view_name="subcategory-detail",
        lookup_field="subcategory_name",
    )

    category = categoryTranslator(
        queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Subcategory
        fields = ("id", "category", "subcategory_name")


class SubcategoryCreateSerializer(ModelSerializer):
    category = categoryTranslator(
        queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Subcategory
        fields = ("category", "subcategory_name")


class SubcategoryDetailSerializer(ModelSerializer):
    category = categoryTranslator(
        queryset=Category.objects.all(), slug_field='name')

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
