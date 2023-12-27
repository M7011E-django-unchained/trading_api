from rest_framework import generics
from website.serializer import (
    UserListSerializer,
    UserDetailSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser


class MemberList(generics.ListAPIView):
    permission_classes = [StaffPermission]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [StaffPermission]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "username"
