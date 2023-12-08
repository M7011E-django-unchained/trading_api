from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from website.serializer import (
    SubcategoryListSerializer,
    SubcategoryCreateSerializer,
    SubcategoryDetailSerializer,)
from website.models import Subcategory


class SubcategoryList(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return SubcategoryCreateSerializer
        return self.serializer_class


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryDetailSerializer
    lookup_field = "subcategory_name"
