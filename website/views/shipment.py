from website.serializer import ShipmentSerializer
from website.models import Shipment
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission


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
    serializer_class = ShipmentSerializer
    permission_classes = [ShipmentPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(username=self.request.user)
