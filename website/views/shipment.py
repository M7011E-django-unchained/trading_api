from website.serializer import (
    ShipmentListSerializer,
    ShipmentCreateSerializer,
    ShipmentDetailSerializer,
)

from website.models import Shipment
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework import generics

# Shipment views

# does this really need permissions?
# you can only create a shipment for a auction you have won


class ShipmentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_active
        return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            # auction owner and the auction winner should be able to access
            # the object
            if (obj.username == request.user or
                    obj.auctionID.auctionOwner == request.user):
                return True

        return request.user.is_staff or request.user.is_superuser


class ShipmentStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser


class ShipmentList(ModelViewSet):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentPermission]

    def get_serializer_class(self):
        if self.action == "create":
            return ShipmentCreateSerializer
        return ShipmentListSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(username=self.request.user)


class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShipmentDetailSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(username=self.request.user)


class ShipmentPaid(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.filter(paid=True)
        return Shipment.objects.filter(paid=True, username=self.request.user)


class ShipmentUnpaid(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.filter(paid=False)
        return Shipment.objects.filter(paid=False, username=self.request.user)


class ShipmentShipped(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.filter(shipped=True)
        return Shipment.objects.filter(shipped=True,
                                       username=self.request.user)


class ShipmentUnshipped(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.filter(shipped=False)
        return Shipment.objects.filter(shipped=False,
                                       username=self.request.user)


class ShipmentUserList(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentStaffPermission]

    def get_queryset(self):
        return Shipment.objects.filter(username=self.kwargs["pk"])


class ShipmentByAuction(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    permission_classes = [ShipmentStaffPermission]

    def get_queryset(self):
        return Shipment.objects.filter(auctionID=self.kwargs["pk"])
