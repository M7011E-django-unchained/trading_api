from rest_framework import generics
from website.serializer import (
    UserListSerializer,
    UserDetailSerializer,
    UserDetailLimitedSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_staff or request.user.is_superuser


class MemberList(generics.ListAPIView):
    permission_classes = [StaffPermission]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [StaffPermission]
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return UserDetailSerializer
        return UserDetailLimitedSerializer
