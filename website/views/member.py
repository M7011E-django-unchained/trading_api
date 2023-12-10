from rest_framework import generics
from website.serializer import (
    UserListSerializer,
    UserDetailSerializer,
)
from django.contrib.auth.models import User


class MemberList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class MemberDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "username"
