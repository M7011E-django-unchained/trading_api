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


class ShipmentDetail(generics.RetrieveAPIView):
    serializer_class = ShipmentDetailSerializer
    permission_classes = [ShipmentPermission]
    queryset = Shipment.objects.all()
    lookup_field = "pk"


class ShipmentPaid(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    queryset = Shipment.objects.filter(paid=True)


class ShipmentUnpaid(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    queryset = Shipment.objects.filter(paid=False)


class ShipmentShipped(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    queryset = Shipment.objects.filter(shipped=True)


class ShipmentUnshipped(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    queryset = Shipment.objects.filter(shipped=False)
