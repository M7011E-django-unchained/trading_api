from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from website.serializer import (
    SubcategoryListSerializer,
    SubcategoryCreateSerializer,
    SubcategoryDetailSerializer,)
from website.models import Subcategory


class SubcategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_superuser or request.user.is_staff


class SubcategoryList(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return SubcategoryCreateSerializer
        return self.serializer_class


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SubcategoryPermission]
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryDetailSerializer
    lookup_field = "subcategory_name"
