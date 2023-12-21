from website.serializer import ShipmentSerializer
from website.models import Shipment
from rest_framework.viewsets import ModelViewSet
from .helpers import idempotent_check, IdempotencyException

# Shipment views

# does this really need permissions?
# you can only create a shipment for a auction you have won


class ShipmentList(ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action == "create":
            if idempotent_check(self.request):
                return ShipmentSerializer
            raise IdempotencyException
        return self.serializer_class
