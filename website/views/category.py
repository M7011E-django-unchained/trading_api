
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from website.serializer import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryDetailSerializer,
)
from website.models import Category


class CategoryList(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        return self.serializer_class


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "name"
