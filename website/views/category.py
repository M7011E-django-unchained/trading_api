
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from website.serializer import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryDetailSerializer,
)
from website.models import Category


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_superuser or request.user.is_staff


class CategoryList(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        return self.serializer_class


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CategoryPermission]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "name"
